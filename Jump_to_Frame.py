-----------------------------------------------------------------------
#ver.1.0
-----------------------------------------------------------------------

from ij import IJ, WindowManager
from javax.swing import JFrame, JTextField, JLabel, JPanel
from java.awt import FlowLayout, GridLayout
from java.awt.event import ActionListener

class JumpTool(JFrame, ActionListener):
    def __init__(self):
        # ウィンドウ自体の設定（タイトル、常に最前面、閉じた時の挙動）
        JFrame.__init__(self, "Jump Tool")
        self.setAlwaysOnTop(True)
        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        
        # 縦に3行並べるレイアウトを設定
        self.getContentPane().setLayout(GridLayout(3, 1))

        # --- 1段目：FPS入力行 ---
        p1 = JPanel(FlowLayout(FlowLayout.RIGHT))
        p1.add(JLabel("FPS:"))
        self.field_fps = JTextField("30", 5) # 初期値30、幅5文字
        p1.add(self.field_fps)
        self.add(p1)

        # --- 2段目：フレーム(Frame)入力行 ---
        p2 = JPanel(FlowLayout(FlowLayout.RIGHT))
        p2.add(JLabel("Frame:"))
        self.field_frame = JTextField(5)
        self.field_frame.addActionListener(self) # Enterキーを監視
        p2.add(self.field_frame)
        self.add(p2)

        # --- 3段目：秒数(Sec)入力行 ---
        p3 = JPanel(FlowLayout(FlowLayout.RIGHT))
        p3.add(JLabel("Sec:"))
        self.field_sec = JTextField(5)
        p3.add(self.field_sec)
        self.field_sec.addActionListener(self) # Enterキーを監視
        self.add(p3)

        # ウィンドウを中身に合わせたサイズにして表示
        self.pack()
        self.setLocationRelativeTo(None) # 画面中央に配置
        self.setVisible(True)

    def actionPerformed(self, event):
        imp = WindowManager.getCurrentImage()
        if not imp:
            return

        source = event.getSource() # どの入力欄でEnterが押されたか特定
        try:
            # 現在のFPS設定を取得
            fps = float(self.field_fps.getText())
            
            if source == self.field_frame:
                # フレーム入力欄でEnterが押された場合
                f = int(self.field_frame.getText())
                self.jump(imp, f)
                self.field_frame.selectAll() # 次回入力しやすくするために全選択
            
            elif source == self.field_sec:
                # 秒数入力欄でEnterが押された場合
                sec = float(self.field_sec.getText())
                f = int(round(sec * fps))
                self.jump(imp, f)
                self.field_sec.selectAll() # 全選択
                
        except Exception as e:
            # 数字以外が入った場合などはログに出力
            print("Input Error: ", e)

    def jump(self, imp, f):
        if imp.isHyperStack():
            imp.setT(f) # ハイパースタック（T軸）の場合
        else:
            imp.setSlice(f) # 通常のスタック（Z軸）の場合

# すでに同じウィンドウが開いていたら一旦閉じる（二重起動防止）
old_win = WindowManager.getFrame("Jump Tool")
if old_win:
    old_win.dispose()
    
JumpTool()