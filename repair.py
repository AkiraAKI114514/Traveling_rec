import sqlite3
import io

class Repair():
    def repair_database(self,src_path, dest_path):
        try:
            # 尝试以只读方式打开
            with sqlite3.connect(f'file:{src_path}?mode=ro', uri=True) as src:
                # 创建新数据库
                with sqlite3.connect(dest_path) as dest:
                    # 使用备份API
                    src.backup(dest)
            print(f"成功修复并保存到 {dest_path}")
        except Exception as e:
            print(f"修复失败: {str(e)}")

# 使用示例
if __name__ == "__main__":
    repair = Repair()
    repair.repair_database('travel.db', 'repaired.db')