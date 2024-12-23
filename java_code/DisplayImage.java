import javax.swing.*;
import java.awt.*;
import java.util.Timer;
import java.util.TimerTask;

public class DisplayImage {
    private String imagePath;

    public void setImagePath(String path) {
        this.imagePath = path;
    }

    public void display() {
        JFrame frame = new JFrame("显示图片");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 400);

        // 替换为你的图片路径
        ImageIcon imageIcon = new ImageIcon(imagePath);
        JLabel label = new JLabel(imageIcon);
        frame.add(label);

        frame.setVisible(true);

        // 设置三秒后关闭
        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                frame.dispose();
            }
        }, 3000);
    }
}