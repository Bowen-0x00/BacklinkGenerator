from utils.message import notify
import urllib.request
import json

class Anki:
    def __init__(self, config):
        self.config = config

    def invoke_anki(self, action, **params):
        """调用 Anki-Connect API 的通用函数"""
        request_data = json.dumps({"action": action, "params": params, "version": 6}).encode("utf-8")
        request = urllib.request.Request(self.config.get('Anki', 'url'), data=request_data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request) as response:
            response_body = response.read()
            response_dict = json.loads(response_body.decode("utf-8"))
            if response_dict.get("error") is not None:
                raise Exception(f"Anki API Error: {response_dict['error']}")
            return response_dict.get("result")
            
    def send_to_anki(self, fields_to_update: dict):
        """
        查找最新的Anki笔记并更新指定的字段。

        Args:
            fields_to_update (dict): 一个包含字段名和新值的字典, 例如: {'Sentence': 'some text', 'url': 'http://...'}.
        """
        try:
            print("正在连接Anki并查找最新笔记...")
            all_note_ids = self.invoke_anki("findNotes", query="")
            if not all_note_ids:
                raise Exception("Anki中没有任何笔记。")

            latest_note_id = max(all_note_ids)
            print(f"找到最新笔记ID: {latest_note_id}")

            # 获取笔记现有所有字段的值，以防覆盖
            note_info = self.invoke_anki("notesInfo", notes=[latest_note_id])[0]
            current_fields = {
                field_name: field_data['value'] 
                for field_name, field_data in note_info['fields'].items()
            }
            
            # 使用新数据更新字段
            current_fields.update(fields_to_update)
            
            payload = {
                "note": {
                    "id": latest_note_id,
                    "fields": current_fields
                }
            }
            
            self.invoke_anki("updateNoteFields", **payload)
            
            # 验证并通知
            print(f"成功为笔记 {latest_note_id} 更新字段: {list(fields_to_update.keys())}")
            notify("Anki 更新成功", f"已为最新笔记更新字段。")

        except Exception as e:
            print(f"Anki更新过程中发生错误: {e}")
            notify("Anki 更新失败", f"错误: {e}")

