import java.util.HashMap;
import java.util.Map;
import java.io.*;
import java.net.*;
import java.util.concurrent.*;


public class Main {
    static DisplayImage displayImage = new DisplayImage();
    static DataGet dataGet = new DataGet();
    static MP3Player mp3Player = new MP3Player();
    static Map<String, String> imgPath = new HashMap<>();
    static Map<String, String> mp3Path = new HashMap<>();
    static String key;
    static boolean running = true;
    static char lastKeyPressed;
    static KeyDetector keyDetector = new KeyDetector();

    public static void main(String[] args) {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        executor.submit(() -> {
            try {
                imgPath.put("a", "src/a.png");
                imgPath.put("d", "src/d.png");
                imgPath.put("w", "src/w.png");
                imgPath.put("s", "src/s.png");
                mp3Path.put("a", "src/a.mp3");
                mp3Path.put("d", "src/d.mp3");
                mp3Path.put("w", "src/w.mp3");
                mp3Path.put("s", "src/s.mp3");
                while (running) {
                    try {
                        Thread.sleep(100); // 100毫秒
                        key = null;
                        dataGet.communication();
                        String key = dataGet.getData();
                        if (key != null) {
                            displayImage.setImagePath(imgPath.get(key));
                            displayImage.display();
                            mp3Player.setFilePath(mp3Path.get(key));
                            mp3Player.mp3Player();
                        }
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        });

        try {
            while (true) {
                lastKeyPressed = keyDetector.getLastKeyPressed();
                System.out.println("最后按下的键是: " + lastKeyPressed);
                if (lastKeyPressed == 'q') {
                    running = false;
                    executor.shutdown();
                    System.out.println("Program has been terminated.");
                    break;
                }
            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}