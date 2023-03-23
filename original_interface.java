import java.awt.Canvas;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;

public class Main {
    public static void main(String[] args) throws IOException {
        JFrame frame = new JFrame("try_btn");
        frame.setSize(354, 633);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        ImageIcon bgIcon = new ImageIcon("canuseinterface.PNG");
        Image bgImage = bgIcon.getImage();
        Image scaledBgImage = bgImage.getScaledInstance(500, 400, Image.SCALE_SMOOTH);
        ImageIcon scaledBgIcon = new ImageIcon(scaledBgImage);
        JLabel bgLabel = new JLabel(scaledBgIcon);
        bgLabel.setBounds(0, 0, 500, 400);

        frame.add(bgLabel);

        JButton recipeBtn = new JButton();
        recipeBtn.setBounds(72, 360, 60, 60);
        recipeBtn.setBorderPainted(false);
        recipeBtn.setFocusPainted(false);
        recipeBtn.setContentAreaFilled(false);
        recipeBtn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    Runtime.getRuntime().exec("python recipe_request.py");
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        });

        ImageIcon recipeIcon = new ImageIcon("recipe_icon.png");
        Image recipeImage = recipeIcon.getImage();
        Image scaledRecipeImage = recipeImage.getScaledInstance(60, 60, Image.SCALE_SMOOTH);
        ImageIcon scaledRecipeIcon = new ImageIcon(scaledRecipeImage);
        recipeBtn.setIcon(scaledRecipeIcon);

        frame.add(recipeBtn);

        JButton nutrientBtn = new JButton();
        nutrientBtn.setBounds(240, 360, 60, 60);
        nutrientBtn.setBorderPainted(false);
        nutrientBtn.setFocusPainted(false);
        nutrientBtn.setContentAreaFilled(false);
        nutrientBtn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    Runtime.getRuntime().exec("python d_project.py");
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        });

        ImageIcon nutrientIcon = new ImageIcon("nutrient_icon.png");
        Image nutrientImage = nutrientIcon.getImage();
        Image scaledNutrientImage = nutrientImage.getScaledInstance(60, 60, Image.SCALE_SMOOTH);
        ImageIcon scaledNutrientIcon = new ImageIcon(scaledNutrientImage);
        nutrientBtn.setIcon(scaledNutrientIcon);

        frame.add(nutrientBtn);

        JButton sportBtn = new JButton();
        sportBtn.setBounds(72, 498, 60, 60);
        sportBtn.setBorderPainted(false);
        sportBtn.setFocusPainted(false);
        sportBtn.setContentAreaFilled(false);
        sportBtn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    Runtime.getRuntime().exec("python register.py");
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        });

        ImageIcon sportIcon = new ImageIcon("sport_icon.png");
        Image sportImage = sportIcon.getImage();
        Image scaledSportImage = sportImage.getScaledInstance(60, 60, Image.SCALE_SMOOTH);
        ImageIcon scaledSportIcon = new ImageIcon(scaledSportImage);
        sportBtn.setIcon(scaledSportIcon);

        frame.add(sportBtn);

        JButton projectLinkBtn = new JButton();
        projectLinkBtn.setBounds(240, 498, 60, 60);
        projectLinkBtn.setBorderPainted(false);
        projectLinkBtn.setFocusPainted(false);
        projectLinkBtn.setContentAreaFilled(false);
        projectLinkBtn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String url = "https://www.canva.com/design/DAE7Y9mhbWI/PBOKmoB1WWus2jsTu12KWA/view?utm_content=DAE7Y9mhbWI&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton";
                try {
                    java.awt.Desktop.getDesktop().browse(java.net.URI.create(url));
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        });

        ImageIcon projectLinkIcon = new ImageIcon("project_link_icon.png");
        Image projectLinkImage = projectLinkIcon.getImage();
        Image scaledProjectLinkImage = projectLinkImage.getScaledInstance(60, 60, Image.SCALE_SMOOTH);
        ImageIcon scaledProjectLinkIcon = new ImageIcon(scaledProjectLinkImage);
        projectLinkBtn.setIcon(scaledProjectLinkIcon);

        frame.add(projectLinkBtn);

        frame.setLayout(null);
        frame.setVisible(true);
    }
}
