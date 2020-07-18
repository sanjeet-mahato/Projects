
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

import javax.swing.ImageIcon;
import javax.swing.JPanel;
import javax.swing.Timer;
import java.io.*;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;

public class ChessPlay extends JPanel implements KeyListener, MouseListener, ActionListener{
	
	private ImageIcon titleImage;
	private ImageIcon boardImage;
	private ImageIcon piece;
	private int rowpix,colpix;
	private int clicked=0;
	
	private int search_depth=4;// the depth upto which the minimax search tree explores all possible moves for both the teams 
	
	private int board[][]=new int [8][8];
	private long freezone=0;
	private long redzone=0;
	private long bluezone=0;
	private int promote_index=0;
	private int promoted_piece[][]={{-5,-2,-3,-4},{5,2,3,4}};
	
	private int black_king_checked=0;
	private int white_king_checked=0;
	
	private boolean automatic=true;
	
	private boolean running=true;
	
	private Timer timer;
	private int delay= 1;
	
	private double inf=99999999;//infinity
	
	Board b=null;
	int turn=-1;//-1 corresponds to white's turn and 1 corresponds to black's turn 
	
	public static void PlaySound(File Sound)//method to play chess sound effects 
	{
		try{
				Clip clip=AudioSystem.getClip();
				clip.open(AudioSystem.getAudioInputStream(Sound));
				clip.start();
				Thread.sleep(200);
			}
		catch(Exception e)
			{
			}
	}
	
	public ChessPlay()
	{
		addKeyListener(this);
		setFocusable(true);
		setFocusTraversalKeysEnabled(false);
		initialise();
		timer= new Timer(delay, this);
		timer.start();
	}
	
	public void initialise()
	{
		board[0][0]=-2;//black Rook
		board[0][1]=-4;//black Horse
		board[0][2]=-3;//black Bishop
		board[0][3]=-5;//black Queen
		board[0][4]=-6;//black King
		board[0][5]=-3;//black Bishop
		board[0][6]=-4;//black Horse
		board[0][7]=-2;//black Rook
		for(int i=0;i<8;i++)
			board[1][i]=-1;//black pawn
		for(int i=0;i<8;i++)
			board[6][i]=1;//white pawn
		board[7][0]=2;//white Rook
		board[7][1]=4;//white Horse
		board[7][2]=3;//white Bishop
		board[7][3]=5;//white Queen
		board[7][4]=6;//white King
		board[7][5]=3;//white Bishop
		board[7][6]=4;//white Horse
		board[7][7]=2;//white Rook
	
		b=new Board();
		b.reset();
		setBoard();
		
		
		freezone=0;
		redzone=0;
		bluezone=0;
		promote_index=0;
		black_king_checked=0;
		white_king_checked=0;		
		running=true;
		turn=-1;
	}
	
	void setBoard()
	{
		int change[]= {-2,-4,-3,-5,-6,-3,-4,-2,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,2,4,3,5,6,3,4,2};
		for(int i=0;i<8;i++)
		{
			for(int j=0;j<8;j++)
			{
				board[i][j]=0;
			}
		}
		for(int i=0;i<32;i++)
		{
			if(b.piece[i]!=0)
			{
				int loc=Long.numberOfLeadingZeros(b.piece[i]);
				int x=loc/8;
				int y=loc%8;
				board[x][y]=change[b.designation[i]];
			}
		}
	}
	
	int piece_index(long x)//method returns the chess piece index located at location denoted by 1 in bitwise long x
	{
		int p=-1;
		for(int i=0;i<32;i++)
		{
			if((b.piece[i]&x)!=0)
			{
				p=i;
				break;
			}
		}
		return p;
	}
	
	Board appropriate_call(int j)//method for finding all the legal moves for a piece index j 
	{
		Board temp=null;
		int depth=1;
		int choice;
		
		int i=b.designation[j];
		
		if(i<16)
			choice=1;
		else
			choice=-1;
		
		if(i==0 || i==7 || i==24 || i==31)
    	{
			temp=b.rook(j,choice,depth,-inf,inf);
		}
    	else if(i==1 || i==6 || i==25 || i==30)
    	{
			temp=b.knight(j,choice,depth,-inf,inf);
		}
    	else if(i==2 || i==5 || i==26 || i==29)
    	{
			temp=b.bishop(j,choice,depth,-inf,inf);
		}
    	else if(i==3 || i==27)
    	{
			temp=b.queen(j,choice,depth,-inf,inf);
		}
    	else if(i==4 || i==28)
    	{
			temp=b.king(j,choice,depth,-1,-inf,inf);
		}
    	else if(i>=8 && i<24)
    	{
			temp=b.pawn(j,choice,depth,-inf,inf);
		}
		return temp;
	}
	
	
	void check()//method to find out if the black/white king is at check 
	{
		Board temp=b.minimax(1,0,-inf,inf);
		if(temp!=null && temp.weight<(-b.king_value/2))//if white king would be eliminated if team black is to make a move  
			white_king_checked=1;//then it means white king is already at check 
		else
			white_king_checked=0;
		
		temp=b.minimax(-1,0,-inf,inf);
		if(temp!=null && temp.weight>(b.king_value/2))//if black king would be eliminated if team white is to make a move 
			black_king_checked=1;//then it means black king is already at check 
		else 
			black_king_checked=0;
	}
	
	void users_turn(int lower ,int upper)//method to make a manual player's move 
	{
			int row=(rowpix-128)/70;
			int col=(colpix-19)/70;
			long loc=1;
			loc<<=(63-(8*row+col));
			int index=piece_index(loc);
			
			
			if(clicked==1)//when a piece is selected 
			{
				b.blackComponents();
	        	b.whiteComponents();
	        	redzone=b.whitePos|b.blackPos;// is the zone where one chess piece move would replace another chess piece	
	        	freezone=redzone;//is the zone where a chess piece can legally move without collision 
	        	bluezone=loc;//is the location of chess piece selected to be moved
	        	
	        	
	        	Board temp=null;
	        	
	        	if(index>=lower && index<=upper)
	        	{
	        		b.piece_moved=index;
	        		temp=appropriate_call(index);//find all legal moves for the selected chess piece 
	        	}
	        	
	        	
	        	if(temp!=null && white_king_checked==1 && (index<16 || temp.weight<(-b.king_value/2)))//if its white's turn and a black 
	        		temp=null;// piece is selected or white king is checked and this move eliminates white king, then this move is invalid 
	        	else if(temp!=null && black_king_checked==1 && (index>=16 || temp.weight>(b.king_value/2)))//if its black's turn and a white 
	        		temp=null;// piece is selected or black king is checked and this move eliminates black king, then this move is invalid 
	        	
	        	if((turn==1 && index>=16) || (turn==-1 && index<16))
	        		temp=null;
	        	
	        	if(temp!=null)
	        	{
	        		redzone=temp.states&redzone; 
	        		freezone=temp.states&(~redzone);
	        		if((redzone|freezone)==0)//if no legal moves for the selected piece is available
	        			bluezone=0;//the piece is not selected 
	        		clicked=2;
	        		repaint();
	        	}
	        	else //if a wrong cell is selected which is either a blank cell or contains opponents chess piece 
	        	{
	        		clicked=0;//then another piece has to be selected again
	        		check();
	        		if((white_king_checked==1 && turn==-1) || (black_king_checked==1 && turn==1))
	        		{//if the player's king is at check during this wrong selection, check alert sound is played
	        			File ch=new File("check.wav");
						PlaySound(ch);
	        		}
	        	}
			}
			else if(clicked==3)//when the cell to which the chess piece is to be moved is selected 
			{
				if((loc&(freezone|redzone))!=0)//if the selected cell corresponds to a legal chess move 
				{
					b.piece[b.piece_moved]=loc;//the selected chess piece's location is updated
					if(index!=-1)
						b.piece[index]=0;
					
					int des=b.designation[b.piece_moved];
					if(des>=8 && des<16 && (loc>>>8)==0)//if black pawn is at the last row 
						{
							promote_index=b.piece_moved;//then this piece is to be promoted 
							clicked=4;
						}
					else if(des>=16 && des<24 && (loc<<8)==0)//if white pawn is at the first row 
						{
							promote_index=b.piece_moved;//then this piece is to be promoted 
							clicked=4;
						}
					else
						{
							promote_index=0;//for all other situations there is no promotion 
							if(automatic && turn==-1)//if the game is user vs computer and it is the black's turn now
								clicked=6;//control transfered to the computer to make the next move 
							else
								clicked=0;//else control is transfered to the other user player playing the game 
							setBoard();
							check();
							turn=-turn;
							
							if((((b.minimax(turn,1,-inf,inf)).weight)*turn)>(b.king_value/2))//if checkmate condition is reached
							{
								running=false;//the game comes to an end 
							}
						}
					
					b.whiteComponents();
					b.blackComponents();
					
					if((black_king_checked==1 && turn==1) || (white_king_checked==1 && turn==-1))//if either of king is at check 
					{
						File ch=new File("check.wav");//sound for check alert is played 
						PlaySound(ch);
					}
					else if(((redzone&b.whitePos)!=0 && turn==1) || ((redzone&b.blackPos)!=0 && turn==-1))//if a piece is replaced 
					{
						File rp=new File("replaced.wav");//sound for piece replacement is played 
						PlaySound(rp);
					}
					else
					{
						File pl=new File("placed.wav");//sound for piece placed is played 
						PlaySound(pl);
					}
					
				}
				else if(index>=lower && index<=upper)//if some other chess piece is selected instead of the cell to which already 
					clicked=1;// selected chess piece is to be moved 
				else
					{
						clicked=0;//for wrong selection, the user needs to choose again 
						check();
						if((white_king_checked==1 && turn==-1) || (black_king_checked==1 && turn==1))//if either king at check 
						{
							File ch=new File("check.wav");//sound for check alert is played 
							PlaySound(ch);
						}
						else
						{
							File inv=new File("invalid.wav");//error sound is played denoting wrong cell selection 
							PlaySound(inv);
						}
						
					}
				
				redzone=0;
				freezone=0;
				bluezone=0;
				repaint();
			}
			else if(clicked==5)//if a pawn has reached its end position and is to be promoted 
			{
				if(row==3 && col==3)//this cell is selected to promote pawn to queen  
				{
					int des=3;//black queen by default 
					if(promote_index>=16)//if white's pawn is promoted
						des=27;//then white queen 
					b.designation[promote_index]=des;
					clicked=0;
				}
				else if(row==3 && col==4)//this cell is selected to promote pawn to rook 
				{
					int des=0;//black rook by default 
					if(promote_index>=16)//if white's pawn is promoted 
						des=24;//then white rook
					b.designation[promote_index]=des;
					clicked=0;
				}
				else if(row==4 && col==3)//this cell is selected to promote pawn to bishop 
				{
					int des=2;//black bishop by default 
					if(promote_index>=16)//if white's pawn is promoted 
						des=26;//then white bishop 
					b.designation[promote_index]=des;
					clicked=0;
				}
				else if(row==4 && col==4)//this cell is selected to promote pawn to knight 
				{
					int des=1;//black bishop by default 
					if(promote_index>=16)//if white's pawn is promoted 
						des=25;//then white bishop 
					b.designation[promote_index]=des;
					clicked=0;
				} 
				else
				clicked=4;// if invalid cell is selected then the user needs to select promoted piece again 
				
				if(clicked==0)//if appropriate cell is selected 
				{
					if(automatic && turn==-1)//and it is user vs computer game 
						clicked=6;// the control is transfered to the computer to make the next move 
					
					promote_index=0;
					setBoard();
					check();
					turn=-turn;
					
					if((((b.minimax(turn,1,-inf,inf)).weight)*turn)>(b.king_value/2))//if it result in a checkmate 
					{
						running=false;//the game comes to an end 
					}		
					redzone=0;
					freezone=0;
					bluezone=0;
					repaint();
				}
			}
	}
	
	
	public void getImageVal(int n)//method to acquire the appropriate chess piece image for painting the chess board 
	{
		switch(n)
		{
			case -1:  piece=new ImageIcon("BlackPawn.png");
			break;
			case -2:  piece=new ImageIcon("BlackRook.png");
			break;
			case -3:  piece=new ImageIcon("BlackBishop.png");
			break;
			case -4:  piece=new ImageIcon("BlackKnight.png");
			break;
			case -5:  piece=new ImageIcon("BlackQueen.png");
			break;
			case -6:  piece=new ImageIcon("BlackKing.png");
			break;
			case 1:  piece=new ImageIcon("WhitePawn.png");
			break;
			case 2:  piece=new ImageIcon("WhiteRook.png");
			break;
			case 3:  piece=new ImageIcon("WhiteBishop.png");
			break;
			case 4:  piece=new ImageIcon("WhiteKnight.png");
			break;
			case 5:  piece=new ImageIcon("WhiteQueen.png");
			break;
			case 6:  piece=new ImageIcon("WhiteKing.png");
			break;
			
		}
	}
	
	public void paint(Graphics g)//method to paint the chess board to be displayed 
	{
		g.setColor(Color.white);
		g.drawRect(10,10,561,75);
		
		titleImage=new ImageIcon("chessname.png");
		titleImage.paintIcon(this, g, 11, 11);
		
		g.setColor(Color.white);
		g.drawRect(10,96,561,561);
		
		boardImage=new ImageIcon("ChessBoard.png");
		boardImage.paintIcon(this, g, 11, 97);
		
		g.setColor(Color.white);
		g.setFont(new Font("arial",Font.BOLD,18));
		
		if(turn==1 && running)
			g.drawString("Black's Turn", 440, 54);
		else if(turn==-1 && running)
			g.drawString("White's Turn", 440, 54);
		

		g.setColor(Color.white);
		g.setFont(new Font("arial",Font.BOLD,13));
		
		if(automatic)
			g.drawString("User Vs Computer", 25, 35);
		else
			g.drawString("Player Vs Player", 29, 35);
		
			g.drawString("Press F5", 52, 55);
			g.drawString("to change Mode", 30, 75);
		
		
		if(clicked!=2 && white_king_checked==1)//if white king is at check 
			redzone=b.piece[28];//white king's cell is highlighted in red 
		else if(clicked!=2 && black_king_checked==1)//if black king is at check 
			redzone=b.piece[4];//black king's cell is highlighted in red 
		
		
		String freestring=Long.toBinaryString(freezone);
		while(freestring.length()<64)
			freestring="0"+freestring;//string of bits with 1's denoting cells which are valid positions for selected chess piece  
		String redstring=Long.toBinaryString(redzone);
		while(redstring.length()<64)
			redstring="0"+redstring;//string of bits with 1's denoting cells which are positions of collision for selected chess piece move 
		String bluestring=Long.toBinaryString(bluezone);
		while(bluestring.length()<64)
			bluestring="0"+bluestring;//string of bits with 1's denoting cell where selected chess piece is located 
		int alpha = 150; // 25% transparent
		Color green = new Color(0, 252, 0, alpha);//green color
		Color red = new Color(255, 0, 0, alpha);//red color
		Color blue= new Color(255, 165, 0, alpha);//blue color
		
		for(int i=0;i<64;i++)//highlighting the chess cells with appropriate colour 
		{
			int row=i/8;
			int col=i%8;
			row=row*70+97;
			col=col*70+11;	
			if(freestring.charAt(i)=='1')
			{
				g.setColor(green);
				g.drawRect(col,row,70,70);
				g.fillRect(col,row,70,70);
			}
			else if(redstring.charAt(i)=='1')
			{
				g.setColor(red);
				g.drawRect(col,row,70,70);
				g.fillRect(col,row,70,70);
			}
			else if(bluestring.charAt(i)=='1')
			{
				g.setColor(blue);
				g.drawRect(col,row,70,70);
				g.fillRect(col,row,70,70);
			}
		}
		
		
		for(int i=0;i<64;i++)//painting appropriate chess icons in the chess cells 
		{
			int row=i/8;
			int col=i%8;
			int x=board[row][col];
			if(x!=0)
			{
			getImageVal(x);
			row=row*70+101;
			col=col*70+15;
			piece.paintIcon(this, g, col, row);
			}
		}
		
		if(promote_index!=0)//if a pawn is to be promoted 
		{
			g.setColor( new Color(128, 128, 0, alpha));
			g.fillRect(11,97,560,560);
			
			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.BOLD,14));
			g.drawString("Choose new promoted piece", 190, 290);
			
			g.setColor(new Color(0,255,255));
			g.fillRect(221,307,70,70);
			
			g.fillRect(291,377,70,70);
			

			g.setColor(new Color(0,128,128));
			g.fillRect(291,307,70,70);
			
			g.fillRect(221,377,70,70);
			
			int temp=1;
			if(promote_index<16)
			temp=0;
				//painting all the pieces to be choosen from for promotion 
				getImageVal(promoted_piece[temp][0]);
				piece.paintIcon(this, g,225,311);
				getImageVal(promoted_piece[temp][1]);
				piece.paintIcon(this, g,295,311);
				getImageVal(promoted_piece[temp][2]);
				piece.paintIcon(this, g,225,381);
				getImageVal(promoted_piece[temp][3]);
				piece.paintIcon(this, g,295,381);
		}
		
		if(!running)//if the game comes to an end 
		{
			g.setColor( new Color(128, 128, 0, 150));
			g.fillRect(11,97,560,560); 
		
			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.BOLD,40));
			g.drawString("GAME OVER", 170, 360);
		
			if(black_king_checked==1)//if black king is checked 
			{
				g.setFont(new Font("arial",Font.BOLD,24));
				g.drawString("Checkmate! White Wins", 156, 390);
			}
			else if(white_king_checked==1)//if white king is checked 
			{
				g.setFont(new Font("arial",Font.BOLD,24));
				g.drawString("Checkmate! Black Wins", 156, 390);
			}
			else
			{
				g.setFont(new Font("arial",Font.BOLD,24));
				g.drawString("Game ends in a Draw", 170, 390);
			}

			File over=new File("Game_Over.wav");//sound for game over is played 
			PlaySound(over);
			
			g.setFont(new Font("arial",Font.BOLD,24));
			g.drawString("Press ESCAPE to Restart", 148, 420);
		}
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		timer.start();
		if(running)
		{
		if(clicked==1 || clicked==3 || clicked==5)//if it is user's turn or the game is player vs player 
			users_turn(0,31);
		else if(clicked==6)//if computer has to make a move against the user 
		{
			Board temp=new Board(b.piece,b.designation);
			temp.blackComponents();
			temp.whiteComponents();
			redzone=temp.whitePos|temp.blackPos;
			
			Board find_legal=new Board(b.piece,b.designation);
			find_legal=find_legal.king(4, 1, 1, -1,-inf,inf);//find the best move the black king can make 
			
			long legal_moves_king=0;
			if(find_legal!=null)//if black king has any legal moves to make
				legal_moves_king=find_legal.states;//store all the legal moves possible for the black king 
			
			temp.black_king_legal=legal_moves_king;//these legal states can only be choosen from for the black king 
			
			temp=temp.minimax(1, search_depth,-inf,inf);//find the best chess move that black can take
			bluezone=b.piece[temp.piece_moved];
			b=temp;
			b.blackComponents();
			b.whiteComponents();
			
			freezone=b.states&(~redzone);
			redzone=b.states&(~freezone);
			repaint();//highlight all the legal positions the selected black chess piece can make 
			clicked=7;
			
		}
		else if(clicked==7)
		{
			
			try {
				Thread.sleep(500);
			} catch (InterruptedException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}//wait for 0.5 seconds before making the move 
			
			setBoard();
			check();
			
			if(white_king_checked==1)//if the move places the white king in check 
			{
				File ch=new File("check.wav");//sound for check alert is played 
				PlaySound(ch);
			}
			else if((redzone&b.blackPos)!=0)
			{
				File rp=new File("replaced.wav");//if the move replaces opponent's chess piece 
				PlaySound(rp);//sound for replaced is played 
			}
			else
			{
				File pl=new File("placed.wav");//sound for chess piece placed is played 
				PlaySound(pl);
			}
			
			turn=-turn;//white's turn now 
			if((((b.minimax(turn,1,-inf,inf)).weight)*turn)>(b.king_value/2))//if there is a checkmate 
			{
				running=false;//game comes to an end 
			}
			redzone=0;
			freezone=0;
			bluezone=0;
			repaint();
			clicked=0;
		}
		}
	}

	@Override
	public void keyPressed(KeyEvent e) {
		if(e.getKeyCode()==KeyEvent.VK_F5 && running)//F5 key is used to switch between player vs player
		{//                               							and player vs computer 
			if(automatic)
				automatic=false;
			else
				automatic=true;
			initialise();
			repaint();
		}
		
		if(e.getKeyCode()==KeyEvent.VK_ESCAPE)//escape key is used to reset the game 
		{
			initialise();
			repaint();
		}
		
	}

	@Override
	public void keyReleased(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void keyTyped(KeyEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseClicked(MouseEvent e) {
		//System.out.println("mouse clicked");
	  if(running)
	  {
		colpix=e.getX();
		rowpix=e.getY();
		if(clicked==0)
			clicked=1;//register mouse click when a chess piece is selected 
		else if(clicked==2)
			clicked=3;//register mouse click when the cell to which the chess piece is to moved is selected 
		else if(clicked==4)
			clicked=5;//register mouse click when the chess piece to which the pawn is to be promoted is selected 
	  }
	}

	@Override
	public void mouseEntered(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseExited(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mousePressed(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void mouseReleased(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

}

