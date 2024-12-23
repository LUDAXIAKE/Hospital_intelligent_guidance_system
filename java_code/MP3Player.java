import javazoom.jl.decoder.JavaLayerException;
import javazoom.jl.player.Player;
import java.io.FileInputStream;
import java.io.FileNotFoundException;

public class MP3Player {
    private String filePath;

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public void mp3Player() {
        try {
            FileInputStream fileInputStream = new FileInputStream(filePath);
            Player player = new Player(fileInputStream);
            player.play();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (JavaLayerException e) {
            e.printStackTrace();
        }
    }
}