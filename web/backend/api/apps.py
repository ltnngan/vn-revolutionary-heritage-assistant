# api/apps.py

from django.apps import AppConfig
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        """Auto-load model khi Django server khởi động"""
        # Chỉ chạy khi start server, bỏ qua migrate/makemigrations
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        checkpoint_dir = self._get_checkpoint_path()
        
        print(f"\nTìm checkpoint tại: {checkpoint_dir}")
        
        if os.path.exists(checkpoint_dir):
            self._load_model(checkpoint_dir)
        else:
            self._show_debug_info(checkpoint_dir)
    
    def _get_checkpoint_path(self):
        """Lấy đường dẫn checkpoint"""
        # Từ backend/api/ lùi về root, vào training/vqa_model/vit-phobert-vit5
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        checkpoint_dir = os.path.join(base_dir, '..', '..', 'training', 'vqa_model', 'vit-phobert-vit5')
        return os.path.normpath(checkpoint_dir)
    
    def _load_model(self, checkpoint_dir):
        """Load model vào memory"""
        from api.model_loader import model_inference
        
        print("\n" + "=" * 60)
        print("ĐANG AUTO-LOAD MODEL...")
        print("=" * 60)
        
        try:
            model_inference.load_model(checkpoint_dir)
            print("Model đã load thành công!")
        except Exception as e:
            print(f"Lỗi khi load model: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("=" * 60 + "\n")
    
    def _show_debug_info(self, checkpoint_dir):
        """Hiển thị thông tin debug khi không tìm thấy checkpoint"""
        print(f"\nKhông tìm thấy checkpoint: {checkpoint_dir}")
        print("Kiểm tra lại đường dẫn!\n")
        
        # List nội dung thư mục cha để debug
        parent_dir = os.path.dirname(checkpoint_dir)
        if os.path.exists(parent_dir):
            print(f"Nội dung của {parent_dir}:")
            try:
                for item in os.listdir(parent_dir):
                    print(f"  - {item}")
            except Exception:
                pass
            print()