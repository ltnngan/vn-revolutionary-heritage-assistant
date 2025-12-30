# api/management/commands/load_model.py

from django.core.management.base import BaseCommand
from django.conf import settings
from api.model_loader import model_inference
import os
import traceback


class Command(BaseCommand):
    help = 'Load VQA model vào memory để sẵn sàng phục vụ requests'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--checkpoint',
            type=str,
            default=None,
            help='Đường dẫn checkpoint directory (mặc định lấy từ settings)'
        )
    
    def handle(self, *args, **options):
        # Lấy đường dẫn checkpoint
        checkpoint_dir = options['checkpoint'] or str(settings.VQA_CONFIG['CHECKPOINT_DIR'])
        self.stdout.write(f'Checkpoint directory: {checkpoint_dir}')
        
        # Kiểm tra thư mục tồn tại
        if not os.path.exists(checkpoint_dir):
            self.stdout.write(self.style.ERROR(f'Không tìm thấy: {checkpoint_dir}'))
            self.stdout.write(self.style.WARNING('Hãy copy checkpoint từ Kaggle về thư mục này'))
            return
        
        # Kiểm tra các file cần thiết
        if not self._check_required_files(checkpoint_dir):
            return
        
        # Load model
        self._load_model(checkpoint_dir)
    
    def _check_required_files(self, checkpoint_dir):
        """Kiểm tra các file/thư mục bắt buộc"""
        self.stdout.write('Đang kiểm tra files...')
        
        required_files = {
            'best_checkpoint.pt': 'file',
            'best_vit_lora.pt': 'file',
            'best_phobert_lora': 'dir',
            'best_vit5_lora': 'dir'
        }
        
        missing = []
        for name, type_ in required_files.items():
            path = os.path.join(checkpoint_dir, name)
            
            if type_ == 'file' and not os.path.isfile(path):
                missing.append(f'{name} (file)')
            elif type_ == 'dir' and not os.path.isdir(path):
                missing.append(f'{name} (directory)')
        
        if missing:
            self.stdout.write(self.style.ERROR('Thiếu files:'))
            for item in missing:
                self.stdout.write(f'   - {item}')
            return False
        
        self.stdout.write(self.style.SUCCESS('Tất cả files đều OK'))
        return True
    
    def _load_model(self, checkpoint_dir):
        """Load model vào memory"""
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('Đang load model...')
        self.stdout.write('=' * 60)
        
        try:
            model_inference.load_model(checkpoint_dir)
            
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write(self.style.SUCCESS('Model đã load xong!'))
            self.stdout.write(self.style.SUCCESS('Backend sẵn sàng'))
            self.stdout.write('=' * 60 + '\n')
            
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f'\nKhông tìm thấy file: {e}'))
            traceback.print_exc()
            
        except RuntimeError as e:
            self.stdout.write(self.style.ERROR(f'\nLỗi runtime: {e}'))
            self.stdout.write(self.style.WARNING('Kiểm tra GPU hoặc RAM'))
            traceback.print_exc()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nLỗi: {e}'))
            traceback.print_exc()