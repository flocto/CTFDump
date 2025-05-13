package defpackage;

import java.awt.FlowLayout;
import java.awt.Font;
import java.net.Socket;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.Scanner;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

/* renamed from: JavaIsland  reason: default package */
/* loaded from: game.jar:JavaIsland.class */
class JavaIsland {
    private static JFrame frame = new JFrame();
    private static JLabel story = new JLabel();
    private static JButton button1 = new JButton();
    private static JButton button2 = new JButton();
    private static int state = 0;
    private static int prevState = 0;
    private static boolean hasGlove = false;
    private static String exploit = "";
    private static ArrayList<Integer> history = new ArrayList<>();

    JavaIsland() {
    }

    private static void updateGame() {
        switch (state) {
            case 0:
                if (prevState == 2) {
                    story.setText("<html>You want nothing to do with that lever and back away from it. The computer and lever still sit menacingly in the room.</html>");
                } else if (prevState == 1) {
                    story.setText("<html>It's important to limit your screen time, or at least that's what your doctor told you. You back away from the computer. Surprisigly, the computer immediately turned off again after stepping away from it. The computer and lever still sit menacingly in the room.</html>");
                } else if (prevState == 6) {
                    story.setText("<html>You run away from the hissing vent, but nothing seems to have happened. The computer and lever still sit menacingly in the room.</html>");
                } else {
                    story.setText("<html>You wake up in a musty room with no lighting except a squeaky lamp hanging from the center of the ceiling. You remember nothing other than the fact that your name is Benson Liu and that you're on a quest to become the greatest hacker in the world. You look around the room and see a decrepit Dell workstation in the corner and a rusty lever on the opposite wall.</html>");
                }
                button1.setText("Inspect the computer");
                button2.setText("Inspect the lever");
                return;
            case 1:
                if (!hasGlove) {
                    story.setText("<html>You walk up to the computer and reach for the power button. Before your hand even reaches the power button, the computer springs to life with a concerningly loud hum. The screen says \"WELCOME bliutech\" on it with a green button that says \"LOG IN\".</html>");
                    button1.setText("Click the button");
                    button2.setText("Back away");
                    return;
                }
                story.setText("<html>While you're next to the computer, a distinct smell in the air makes you come to a realization: the hissing sound from the vent was from the release of toxic gas. Unfortunately, you realized this too late as you become light-headed before passing out. Game over.</html>");
                button1.setText("I understand");
                button2.setText("I understand");
                return;
            case 2:
                story.setText("<html>As you walk closer to the lever you realize that it's completely covered in spider webs.</html>");
                button1.setText("Pull the lever");
                button2.setText("Back away");
                return;
            case 3:
                if (!hasGlove) {
                    story.setText("<html>You reach for the lever, plunging your hand into the thick veil of spider webs. While trying to pull the lever, you feel a sharp pain on your arm before your vision fades to black. Game over.</html>");
                    button1.setText("I understand");
                    button2.setText("I understand");
                    return;
                }
                story.setText("<html>You reach for the lever, plunging your gloved hand into the thick veil of spider webs. The lever makes a loud creaking sound as you press it down, powering a large floodlight that lights up the entire room. When you look at your hand in the newfound light, you see several large spiders climbing on your glove. Startled, you shake the glove off and run to the other corner of the room, where you see a flag that must've been there the entire time.</html>");
                button1.setText("Read the flag");
                button2.setText("Read the flag");
                return;
            case 4:
                story.setText("<html>As soon as you click the button, a pair of handcuffs locks you to the table. There's no backing out now. The computer loads a website belong to X Enterprises: a multinational corporation that hates puppies! You have to hack them otherwise puppies all over the world will face the wrath of X Enterprises!</html>");
                button1.setText("Clobber the DOM");
                button2.setText("Pollute the prototype");
                return;
            case 5:
                try {
                    Socket socket = new Socket("chall.lac.tf", 31151);
                    String str = "";
                    Iterator<Integer> it = history.iterator();
                    while (it.hasNext()) {
                        str = str + it.next().intValue();
                    }
                    socket.getOutputStream().write((str + "\n").getBytes("UTF-8"));
                    Scanner scanner = new Scanner(socket.getInputStream());
                    story.setText(scanner.nextLine());
                    scanner.close();
                    socket.close();
                } catch (Exception e) {
                    System.err.println(e.getMessage());
                    story.setText("<html>The flag is garbled and unreadable. Contact an admin if you haven't done anything out of the ordinary.</html>");
                }
                button1.setText("Leave");
                button2.setText("Leave");
                return;
            case 6:
                story.setText("<html>As you submit the last exploit, X Enterprise's website goes down. You did it! You're officially the best and coolest hacker in the world. Your hand is released and a yellow kitchen glove is dropped from the ceiling and you put it on. As the computer shuts off and its loud humming comes to a halt, you can hear something quieter in the background: a soft hissing sound coming from the vent next to the computer.</html>");
                hasGlove = true;
                button1.setText("Run away");
                button2.setText("Investigate");
                return;
            case 7:
                story.setText("<html>Your hacking was ineffective, and the firewall in front of X Enterprises has detected malicious activity and IP banned you. You are not the hacker that you wanted to be, and promptly collapse to the ground with grief. Game over.</html>");
                button1.setText("I understand");
                button2.setText("I understand");
                return;
            default:
                return;
        }
    }

    /* JADX INFO: Access modifiers changed from: private */
    public static void transitionState(int i) {
        history.add(Integer.valueOf(i));
        prevState = state;
        switch (state) {
            case 0:
                if (i == 0) {
                    state = 1;
                    break;
                } else {
                    state = 2;
                    break;
                }
            case 1:
                if (hasGlove) {
                    System.exit(0);
                    break;
                } else if (i == 0) {
                    state = 4;
                    break;
                } else {
                    state = 0;
                    break;
                }
            case 2:
                if (i == 0) {
                    state = 3;
                    break;
                } else {
                    state = 0;
                    break;
                }
            case 3:
                if (!hasGlove) {
                    System.exit(0);
                    break;
                } else {
                    state = 5;
                    break;
                }
            case 4:
                if (i == 0) {
                    exploit += "d";
                    story.setText("You clobbered the DOM. That was exploit #" + exploit.length() + ".");
                } else {
                    exploit += "p";
                    story.setText("You polluted the prototype. That was exploit #" + exploit.length() + ".");
                }
                if (exploit.length() == 8) {
                    try {
                        if (!Arrays.equals(MessageDigest.getInstance("SHA-256").digest(exploit.getBytes("UTF-8")), new byte[]{69, 70, -81, -117, -10, 109, 15, 29, 19, 113, 61, -123, -39, 82, -11, -34, 104, -98, -111, 9, 43, 35, -19, 22, 52, -55, -124, -45, -72, -23, 96, -77})) {
                            state = 7;
                        } else {
                            state = 6;
                        }
                        updateGame();
                        return;
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                }
                return;
            case 5:
            case 7:
                System.exit(0);
                break;
            case 6:
                if (i == 0) {
                    state = 0;
                    break;
                } else {
                    state = 1;
                    break;
                }
        }
        updateGame();
    }

    public static void main(String[] strArr) {
        frame.setDefaultCloseOperation(3);
        frame.setSize(500, 500);
        Font font = new Font("sans-serif", 0, 24);
        JPanel jPanel = new JPanel();
        story.setFont(font);
        button1.setFont(font);
        button2.setFont(font);
        jPanel.setLayout(new FlowLayout());
        jPanel.add(button1);
        jPanel.add(button2);
        button1.addActionListener(actionEvent -> {
            transitionState(0);
        });
        button2.addActionListener(actionEvent2 -> {
            transitionState(1);
        });
        frame.getContentPane().add("Center", story);
        frame.getContentPane().add("South", jPanel);
        updateGame();
        frame.setVisible(true);
    }
}