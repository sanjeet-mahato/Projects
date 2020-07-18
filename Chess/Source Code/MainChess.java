import java.awt.Color;
import javax.swing.JFrame;

public class MainChess {
	
	public static void main(String[] args) {
		JFrame obj=new JFrame();
		ChessPlay chessplay=new ChessPlay(); 
		obj.setBounds(10,10,600,707);
		obj.setBackground(Color.DARK_GRAY);
		obj.setResizable(false);
		obj.setVisible(true);
		obj.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		obj.add(chessplay);
		obj.addMouseListener(chessplay);
	}

}
