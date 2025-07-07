from ui.conversion.json.JsonPanel import JsonPanel
import wx
import json
import pyperclip
from loguru import logger


class Json(JsonPanel):
    def __init__(self, parent):
        JsonPanel.__init__(self, parent)
        self.__init_view()

    def doFormat(self, event):
        try:
            logger.info('开始格式化数据')
            json_data = json.loads(self.txt_format_result.GetValue())
        except ValueError:
            self.__show_message('JSON格式错误')
        else:
            formatted_json = json.dumps(json_data, indent=4, sort_keys=True)
            self.txt_format_result.SetValue(formatted_json)
            self.tree_ctrl.DeleteAllItems()
            root = self.tree_ctrl.AddRoot('JSON')
            self.add_json_to_tree(json_data, root)
            self.tree_ctrl.ExpandAll()

    def doClear(self, event):
        self.txt_format_result.SetValue('')
        self.tree_ctrl.DeleteAllItems()

    def __show_message(self, message):
        wx.MessageDialog(self, message, '提示', wx.OK).ShowModal()

    def add_json_to_tree(self, json_data, parent):
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                if isinstance(value, (dict, list)):
                    child = self.tree_ctrl.AppendItem(parent, str(key))
                    self.add_json_to_tree(value, child)
                else:
                    value_str = str(value)
                    if value_str == 'None':
                        value_str = 'null'
                    self.tree_ctrl.AppendItem(parent, f'{key}: {value_str}')
        elif isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, (dict, list)):
                    child = self.tree_ctrl.AppendItem(parent, 'item')
                    self.add_json_to_tree(item, child)
                else:
                    value_str = str(item)
                    self.tree_ctrl.AppendItem(parent, value_str)

    def on_tree_right_click(self, event):
        item = event.GetItem()  # 获取右键点击的Item
        self.tree_ctrl.SelectItem(item)  # 选中该Item
        self.PopupMenu(self.menu)  # 在鼠标右键点击的位置弹出菜单

    def __copy_key(self, event):
        item = self.tree_ctrl.GetSelection()
        value = self.tree_ctrl.GetItemText(item)
        _key, _value = value.split(":", 1)
        pyperclip.copy(_key)
        self.__show_message('复制成功')

    def __copy_value(self, event):
        item = self.tree_ctrl.GetSelection()
        value = self.tree_ctrl.GetItemText(item)
        _key, _value = value.split(":", 1)
        pyperclip.copy(_value)
        self.__show_message('复制成功')

    def __init_view(self):
        self.txt_format_result.SetForegroundColour(wx.BLUE)
        self.tree_ctrl.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_tree_right_click)
        self.menu = wx.Menu()
        self.menu1 = self.menu.Append(-1, "复制Key")
        self.menu2 = self.menu.Append(-1, "复制Value")
        self.Bind(wx.EVT_MENU, self.__copy_key, self.menu1)
        self.Bind(wx.EVT_MENU, self.__copy_value, self.menu2)
