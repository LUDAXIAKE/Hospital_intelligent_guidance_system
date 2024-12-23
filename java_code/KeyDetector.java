import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import javax.swing.JFrame;

public class KeyDetector extends JFrame implements KeyListener {

    private char lastKeyPressed;

    public KeyDetector() {
        this.setTitle("Key Detector");
        this.setSize(300, 200);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.addKeyListener(this);
        this.setVisible(true);
    }

    @Override
    public void keyTyped(KeyEvent e) {
        // This method is not used but must be implemented
    }

    @Override
    public void keyPressed(KeyEvent e) {
        lastKeyPressed = e.getKeyChar();
        System.out.println("Key Pressed: " + lastKeyPressed);
    }

    @Override
    public void keyReleased(KeyEvent e) {
        // This method is not used but must be implemented
    }

    public char getLastKeyPressed() {
        return lastKeyPressed;
    }
}