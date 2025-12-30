# api/model_loader.py

import torch
import torch.nn as nn
import math
import os
from transformers import (
    ViTModel, ViTImageProcessor,
    AutoModel, AutoTokenizer,
    AutoModelForSeq2SeqLM,
)
from transformers.modeling_outputs import BaseModelOutput
from peft import PeftModel
from PIL import Image
from pyvi import ViTokenizer
import warnings

warnings.filterwarnings('ignore')


# ========================================================================
# CONFIG
# ========================================================================

class Config:
    """Cấu hình model"""
    # Base models
    VIT_MODEL = 'google/vit-base-patch16-224'
    PHOBERT_MODEL = 'vinai/phobert-base'
    VIT5_MODEL = 'VietAI/vit5-base'
    
    # Architecture
    HIDDEN_SIZE = 768
    NUM_ATTENTION_HEADS = 8
    FUSION_DROPOUT = 0.15
    
    # LoRA configs
    LORA_VIT_R = 16
    LORA_VIT_ALPHA = 32
    LORA_VIT_DROPOUT = 0.15
    
    LORA_PHOBERT_R = 16
    LORA_PHOBERT_ALPHA = 32
    LORA_PHOBERT_DROPOUT = 0.15
    
    LORA_VIT5_R = 16
    LORA_VIT5_ALPHA = 32
    LORA_VIT5_DROPOUT = 0.15
    
    # Training settings
    USE_LORA = True
    FUSION_STRATEGY = "gating"
    
    # Sequence lengths
    MAX_QUESTION_LEN = 128
    MAX_ANSWER_LEN = 128
    
    # Generation params
    GEN_MAX_LENGTH = 128
    GEN_MIN_LENGTH = 3
    GEN_NUM_BEAMS = 3
    GEN_NO_REPEAT_NGRAM = 2
    GEN_LENGTH_PENALTY = 0.8
    GEN_REPETITION_PENALTY = 1.2


# ========================================================================
# WORD SEGMENTER
# ========================================================================

class WordSegmenter:
    """Tách từ tiếng Việt (singleton)"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("   ✓ PyVi tokenizer ready")
        return cls._instance
    
    def segment(self, text):
        """Tách từ văn bản tiếng Việt"""
        try:
            return ViTokenizer.tokenize(text)
        except Exception as e:
            print(f"Warning: Lỗi tách từ - {e}")
            return text


# ========================================================================
# CROSS MODAL ATTENTION
# ========================================================================

class CrossModalAttention(nn.Module):
    """Cross-attention giữa visual và text"""
    
    def __init__(self, hidden_size, num_heads, dropout=0.1):
        super().__init__()
        self.multihead_attn = nn.MultiheadAttention(
            embed_dim=hidden_size,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True
        )
        self.norm = nn.LayerNorm(hidden_size)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, query, key_value, key_padding_mask=None):
        """Cross-attention với residual connection"""
        attn_output, _ = self.multihead_attn(
            query, key_value, key_value,
            key_padding_mask=key_padding_mask
        )
        return self.norm(query + self.dropout(attn_output))


# ========================================================================
# FUSION MODULE
# ========================================================================

class FusionModule(nn.Module):
    """Kết hợp visual và text features với gating mechanism"""
    
    def __init__(self, config):
        super().__init__()
        self.strategy = config.FUSION_STRATEGY
        
        # Bi-directional cross-attention
        self.v2q_attention = CrossModalAttention(
            config.HIDDEN_SIZE, config.NUM_ATTENTION_HEADS, config.FUSION_DROPOUT
        )
        self.q2v_attention = CrossModalAttention(
            config.HIDDEN_SIZE, config.NUM_ATTENTION_HEADS, config.FUSION_DROPOUT
        )
        
        # Gating network
        if self.strategy == "gating":
            self.gate = nn.Sequential(
                nn.Linear(config.HIDDEN_SIZE * 2, config.HIDDEN_SIZE),
                nn.ReLU(),
                nn.Dropout(config.FUSION_DROPOUT),
                nn.Linear(config.HIDDEN_SIZE, 1),
                nn.Sigmoid()
            )
        
        # Final projection
        self.projection = nn.Sequential(
            nn.Linear(config.HIDDEN_SIZE, config.HIDDEN_SIZE),
            nn.LayerNorm(config.HIDDEN_SIZE),
            nn.Dropout(config.FUSION_DROPOUT)
        )
    
    def forward(self, visual_features, question_features, question_mask):
        """Fuse visual và question features"""
        question_padding_mask = (question_mask == 0)
        
        # Cross-attention 2 chiều
        attended_question = self.v2q_attention(
            query=question_features,
            key_value=visual_features,
            key_padding_mask=None
        )
        
        attended_visual = self.q2v_attention(
            query=visual_features,
            key_value=question_features,
            key_padding_mask=question_padding_mask
        )
        
        # Gating mechanism
        if self.strategy == "gating":
            vis_pooled = attended_visual.mean(dim=1)
            q_pooled = attended_question.mean(dim=1)
            gate_input = torch.cat([vis_pooled, q_pooled], dim=-1)
            gate_weight = self.gate(gate_input)
            
            attended_visual = attended_visual * gate_weight.unsqueeze(1)
            attended_question = attended_question * (1 - gate_weight.unsqueeze(1))
        
        # Concatenate và project
        fused = torch.cat([attended_visual, attended_question], dim=1)
        return self.projection(fused)


# ========================================================================
# VIT WITH LORA
# ========================================================================

class ViTWithLoRA(nn.Module):
    """ViT với LoRA adapters trên Q, K, V"""
    
    def __init__(self, vit_model, r=8, alpha=16, dropout=0.1):
        super().__init__()
        self.vit = vit_model
        self.r = r
        self.alpha = alpha
        self.scaling = alpha / r
        
        self.lora_layers = nn.ModuleDict()
        
        # Tạo LoRA layers cho mỗi attention layer
        for i, layer in enumerate(self.vit.encoder.layer):
            query_layer = layer.attention.attention.query
            in_features = query_layer.in_features
            out_features = query_layer.out_features
            
            # LoRA cho Query, Key, Value
            for param in ['query', 'key', 'value']:
                self.lora_layers[f'layer_{i}_{param}_A'] = nn.Linear(in_features, r, bias=False)
                self.lora_layers[f'layer_{i}_{param}_B'] = nn.Linear(r, out_features, bias=False)
                
                # Init weights
                nn.init.kaiming_uniform_(self.lora_layers[f'layer_{i}_{param}_A'].weight, a=math.sqrt(5))
                nn.init.zeros_(self.lora_layers[f'layer_{i}_{param}_B'].weight)
        
        self.dropout = nn.Dropout(dropout)
        
        # Freeze base model
        for param in self.vit.parameters():
            param.requires_grad = False
    
    def forward(self, pixel_values):
        """Forward pass với LoRA injection"""
        hooks = []
        
        def make_lora_hook(layer_idx, param_name):
            """Tạo hook để inject LoRA output"""
            def hook(module, input, output):
                lora_A = self.lora_layers[f'layer_{layer_idx}_{param_name}_A']
                lora_B = self.lora_layers[f'layer_{layer_idx}_{param_name}_B']
                x = input[0]
                lora_output = lora_B(lora_A(self.dropout(x))) * self.scaling
                return output + lora_output
            return hook
        
        # Register hooks
        for i, layer in enumerate(self.vit.encoder.layer):
            h1 = layer.attention.attention.query.register_forward_hook(make_lora_hook(i, 'query'))
            h2 = layer.attention.attention.key.register_forward_hook(make_lora_hook(i, 'key'))
            h3 = layer.attention.attention.value.register_forward_hook(make_lora_hook(i, 'value'))
            hooks.extend([h1, h2, h3])
        
        # Forward pass
        outputs = self.vit(pixel_values=pixel_values)
        
        # Remove hooks
        for hook in hooks:
            hook.remove()
        
        return outputs


# ========================================================================
# LOADED MODEL
# ========================================================================

class LoadedModel(nn.Module):
    """Model đầy đủ sau khi load checkpoint"""
    
    def __init__(self, vit, phobert, vit5, fusion, projection, config):
        super().__init__()
        self.vit = vit
        self.phobert = phobert
        self.vit5 = vit5
        self.fusion = fusion
        self.fusion_to_vit5 = projection
        self.config = config
        self.pad_token_id = vit5.config.pad_token_id or 0
    
    def forward(self, pixel_values, question_input_ids, question_attention_mask, 
                answer_input_ids=None, answer_attention_mask=None):
        """Forward pass: image + question -> answer"""
        batch_size = pixel_values.size(0)
        
        # 1. Extract visual features
        vit_outputs = self.vit(pixel_values=pixel_values)
        visual_features = vit_outputs.last_hidden_state[:, 1:, :]  # Bỏ CLS token
        
        # 2. Extract question features
        phobert_outputs = self.phobert(
            input_ids=question_input_ids,
            attention_mask=question_attention_mask
        )
        question_features = phobert_outputs.last_hidden_state
        
        # 3. Fuse visual + question
        fused_features = self.fusion(visual_features, question_features, question_attention_mask)
        fused_features = self.fusion_to_vit5(fused_features)
        
        # 4. Tạo attention mask cho fused features
        num_visual_tokens = fused_features.size(1) - question_attention_mask.size(1)
        visual_mask = torch.ones(batch_size, num_visual_tokens, dtype=torch.long, device=fused_features.device)
        fused_attention_mask = torch.cat([visual_mask, question_attention_mask], dim=1)
        
        # 5. Encoder outputs cho ViT5
        encoder_outputs = BaseModelOutput(last_hidden_state=fused_features)
        
        # 6. Training vs Inference
        if answer_input_ids is not None:
            # Training mode: compute loss
            labels = answer_input_ids.clone()
            labels[labels == self.pad_token_id] = -100
            
            return self.vit5(
                attention_mask=fused_attention_mask,
                encoder_outputs=encoder_outputs,
                labels=labels,
                return_dict=True
            )
        else:
            # Inference mode: generate answer
            return self.vit5.generate(
                encoder_outputs=encoder_outputs,
                attention_mask=fused_attention_mask,
                max_length=self.config.GEN_MAX_LENGTH,
                min_length=self.config.GEN_MIN_LENGTH,
                num_beams=self.config.GEN_NUM_BEAMS,
                early_stopping=True,
                no_repeat_ngram_size=self.config.GEN_NO_REPEAT_NGRAM,
                length_penalty=self.config.GEN_LENGTH_PENALTY,
                repetition_penalty=self.config.GEN_REPETITION_PENALTY,
                do_sample=False
            )


# ========================================================================
# MODEL INFERENCE
# ========================================================================

class ModelInference:
    """Singleton để load và sử dụng model"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.vit_processor = None
        self.phobert_tokenizer = None
        self.vit5_tokenizer = None
        self.segmenter = None
        self.config = None
        
        self._initialized = True
    
    def load_model(self, checkpoint_dir):
        """Load model từ checkpoint"""
        print(f"Loading model from {checkpoint_dir}...")
        print("=" * 60)
        
        # 1. Word segmenter
        print("1. Loading segmenter...")
        self.segmenter = WordSegmenter()
        
        # 2. Tokenizers
        print("2. Loading tokenizers...")
        self.vit_processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
        self.phobert_tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')
        self.vit5_tokenizer = AutoTokenizer.from_pretrained('VietAI/vit5-base')
        print("   ✓ Tokenizers ready")
        
        # 3. Config
        self.config = Config()
        
        # 4. Load checkpoint
        checkpoint_path = os.path.join(checkpoint_dir, 'best_checkpoint.pt')
        self._validate_file(checkpoint_path, "Main checkpoint")
        
        print(f"3. Loading checkpoint...")
        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        print("   ✓ Checkpoint loaded")
        
        # 5. Load base models
        print("4. Loading base models...")
        vit_base = ViTModel.from_pretrained(self.config.VIT_MODEL)
        phobert_base = AutoModel.from_pretrained(self.config.PHOBERT_MODEL)
        vit5_base = AutoModelForSeq2SeqLM.from_pretrained(self.config.VIT5_MODEL)
        print("   ✓ Base models ready")
        
        # 6. Build ViT with LoRA
        print("5. Building ViT with LoRA...")
        vit_with_lora = self._build_vit_lora(vit_base, checkpoint_dir)
        
        # 7. Load PhoBERT with LoRA
        print("6. Loading PhoBERT with LoRA...")
        phobert_with_lora = self._load_phobert_lora(phobert_base, checkpoint_dir)
        
        # 8. Load ViT5 with LoRA
        print("7. Loading ViT5 with LoRA...")
        vit5_with_lora = self._load_vit5_lora(vit5_base, checkpoint_dir)
        
        # 9. Load Fusion
        print("8. Loading Fusion module...")
        fusion = FusionModule(self.config)
        fusion.load_state_dict(checkpoint['fusion'])
        print("   ✓ Fusion ready")
        
        # 10. Load Projection
        print("9. Loading Projection layer...")
        vit5_dim = vit5_with_lora.config.d_model
        projection = nn.Linear(self.config.HIDDEN_SIZE, vit5_dim)
        projection.load_state_dict(checkpoint['projection'])
        print("   ✓ Projection ready")
        
        # 11. Assemble model
        print("10. Assembling model...")
        self.model = LoadedModel(
            vit_with_lora,
            phobert_with_lora,
            vit5_with_lora,
            fusion,
            projection,
            self.config
        )
        
        self.model.to(self.device)
        self.model.eval()
        
        print(f"\n✓ Model ready on {self.device}")
        print("=" * 60 + "\n")
    
    def _validate_file(self, path, name):
        """Kiểm tra file tồn tại"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"{name} not found: {path}")
    
    def _build_vit_lora(self, vit_base, checkpoint_dir):
        """Build ViT với LoRA"""
        vit_with_lora = ViTWithLoRA(
            vit_base,
            r=self.config.LORA_VIT_R,
            alpha=self.config.LORA_VIT_ALPHA,
            dropout=self.config.LORA_VIT_DROPOUT
        )
        
        vit_lora_path = os.path.join(checkpoint_dir, 'best_vit_lora.pt')
        self._validate_file(vit_lora_path, "ViT LoRA")
        
        vit_with_lora.lora_layers.load_state_dict(
            torch.load(vit_lora_path, map_location=self.device)
        )
        print("   ✓ ViT LoRA ready")
        return vit_with_lora
    
    def _load_phobert_lora(self, phobert_base, checkpoint_dir):
        """Load PhoBERT với LoRA"""
        phobert_path = os.path.join(checkpoint_dir, 'best_phobert_lora')
        self._validate_file(phobert_path, "PhoBERT LoRA")
        
        phobert_with_lora = PeftModel.from_pretrained(
            phobert_base,
            phobert_path,
            is_trainable=False
        )
        print("   ✓ PhoBERT LoRA ready")
        return phobert_with_lora
    
    def _load_vit5_lora(self, vit5_base, checkpoint_dir):
        """Load ViT5 với LoRA"""
        vit5_path = os.path.join(checkpoint_dir, 'best_vit5_lora')
        self._validate_file(vit5_path, "ViT5 LoRA")
        
        vit5_with_lora = PeftModel.from_pretrained(
            vit5_base,
            vit5_path,
            is_trainable=False
        )
        print("   ✓ ViT5 LoRA ready")
        return vit5_with_lora
    
    @torch.no_grad()
    def predict(self, image_path, question):
        """Dự đoán câu trả lời từ ảnh và câu hỏi"""
        if self.model is None:
            raise ValueError("Model chưa load. Gọi load_model() trước.")
        
        self.model.eval()
        
        # 1. Load và preprocess ảnh
        try:
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            raise ValueError(f"Không thể load ảnh: {e}")
        
        pixel_values = self.vit_processor(
            images=image,
            return_tensors='pt'
        )['pixel_values'].to(self.device)
        
        # 2. Tách từ câu hỏi
        question_segmented = self.segmenter.segment(question)
        
        # 3. Tokenize câu hỏi
        question_enc = self.phobert_tokenizer(
            question_segmented,
            max_length=self.config.MAX_QUESTION_LEN,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        question_input_ids = question_enc['input_ids'].to(self.device)
        question_attention_mask = question_enc['attention_mask'].to(self.device)
        
        # 4. Generate answer
        generated_ids = self.model(
            pixel_values=pixel_values,
            question_input_ids=question_input_ids,
            question_attention_mask=question_attention_mask
        )
        
        # 5. Decode answer
        answer = self.vit5_tokenizer.decode(
            generated_ids[0],
            skip_special_tokens=True
        )
        
        return answer


# ========================================================================
# GLOBAL INSTANCE
# ========================================================================

model_inference = ModelInference()