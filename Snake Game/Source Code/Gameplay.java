import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.Random;
import javax.swing.ImageIcon;
import javax.swing.JPanel;
import javax.swing.Timer;

public class Gameplay extends JPanel implements KeyListener, ActionListener{
	
	private ImageIcon titleImage;
	private int[] snakexlength=new int[750];
	private int[] snakeylength=new int[750];
	
	private int[] enemyxpos= {25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,
			400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800,825,850};
	private int[] enemyypos= {75,100,125,150,175,200,225,250,275,300,325,350,375,
			400,425,450,475,500,525,550,575,600,625};
	
	private ImageIcon enemyimage;
	
	private Random random=new Random();
	
	private int xpos=random.nextInt(34);
	private int ypos=random.nextInt(23);
	
	private int score=0;
	private boolean running=true;
	private boolean automatic=false;
	private boolean end=false;
	
	private boolean left=false;
	private boolean right=false;
	private boolean up=false;
	private boolean down=false;
	
	private int lengthofsnake=3;
	private int moves=0;
	private int map[][]=new int[23][34];
	private int counter[]= {0,0,0,0,0,0};
	
	private ImageIcon rightmouth;
	private ImageIcon upmouth;
	private ImageIcon downmouth;
	private ImageIcon leftmouth;
	
	private Timer timer;
	private int delay= 100;
	private ImageIcon snakeimage; 
	
	
	public Gameplay()
	{
		addKeyListener(this);
		setFocusable(true);
		setFocusTraversalKeysEnabled(false);
		timer= new Timer(delay, this);
		timer.start();
	}
	
	public double value(int des,int loc,double cons)
	{
		if((des-loc)==0)
			return 0;
		else
			return (cons/(des-loc));
	}
	
	void flood(int i,int j,int n)
	{
		map[i][j]=n;
		counter[n]++;
		if(map[(i+22)%23][j]==0)//up
			flood((i+22)%23,j,n);
		if(map[(i+1)%23][j]==0)//down
			flood((i+1)%23,j,n);
		if(map[i][(j+1)%34]==0)//right
			flood(i,(j+1)%34,n);
		if(map[i][(j+33)%34]==0)//left
			flood(i,(j+33)%34,n);
	}
	
	public void mapping()
	{
		for(int i=0;i<23;i++)
		{
			for(int j=0;j<34;j++)
				map[i][j]=0;
		}
		for(int z=0;z<lengthofsnake;z++)
		{
			int foodx=(snakexlength[z])/25-1;
			int foody=25-((snakeylength[z])/25);
			map[22-foody][foodx]=1;
		}
	}
	/*
	public void display_map()
	{
		System.out.println("----------------MAP---------------------");
		for(int i=0;i<23;i++)
		{
			for(int j=0;j<34;j++)
				System.out.print(map[i][j]+" ");
			System.out.println();
		}
		System.out.println("-----------------------------------------");
	}
	*/
	public int random_generator()
	{
		mapping();
		int fill[]=new int[782-lengthofsnake];
		int ktemp=0;
		for(int i=0;i<23;i++)
		{
			for(int j=0;j<34;j++)
			{
				if(map[i][j]!=1)
				{
					fill[ktemp]=(22-i)*34+j;
					ktemp++;
				}
			}
		}
		
		int retval=random.nextInt(782-lengthofsnake);
		retval=fill[retval];
		return retval;
	}
	
	public void update()
	{
		mapping();
		int foodx=xpos;
		int foody=22-ypos;
		int headx=(snakexlength[0])/25-1;
		int heady=25-((snakeylength[0])/25);
		
		counter[2]=0;
		counter[3]=0;
		counter[4]=0;
		counter[5]=0;
		
		int ori=22-heady;
		int orj=headx;
		
		if(map[(ori+22)%23][orj]==0)//up
			flood((ori+22)%23,orj,2);
		
		if(map[(ori+1)%23][orj]==2)//down
			counter[4]=counter[2];
		else if(map[(ori+1)%23][orj]==0)//down
			flood((ori+1)%23,orj,4);
		
		if(map[ori][(orj+1)%34]==2)//right
			counter[3]=counter[2];
		else if(map[ori][(orj+1)%34]==4)//right
			counter[3]=counter[4];
		else if(map[ori][(orj+1)%34]==0)//right
			flood(ori,(orj+1)%34,3);
		
		if(map[ori][(orj+33)%34]==2)//left
			counter[5]=counter[2];
		else if(map[ori][(orj+33)%34]==4)//left
			counter[5]=counter[4];
		else if(map[ori][(orj+33)%34]==3)//left
			counter[5]=counter[3];
		else if(map[ori][(orj+33)%34]==0)//left
			flood(ori,(orj+33)%34,5);
		
		
		
		int best=0;
		for(int i=2;i<=5;i++)
		{
			if(counter[i]>best)
			{
				best=counter[i];
			}
		}
		
		if(right && counter[3]!=best)
		{
			if(counter[2]>=counter[4])
				up=true;
			else 
				down=true;
			right=false;
			best=1;	
		}
		else if(down && counter[4]!=best)
		{
			if(counter[3]>=counter[5])
				right=true;
			else 
				left=true;
			down=false;
			best=1;	
		}
		else if(left && counter[5]!=best)
		{
			if(counter[2]>=counter[4])
				up=true;
			else 
				down=true;
			left=false;
			best=1;	
		}
		else if(up && counter[2]!=best)
		{
			if(counter[3]>=counter[5])
				right=true;
			else 
				left=true;
			up=false;
			best=1;	
		}
		
		
		
		int rangex[]= {0,34,34,0,-34,-34,-34,0,34};
		int rangey[]= {0,0,-23,-23,-23,0,23,23,23};
		double sumx=0;
		double sumy=0;
		double dis=5;
		for(int i=0;i<9;i++)
		{
			sumx+=value(rangex[i]+foodx,headx,dis);
			sumy+=value(rangey[i]+foody,heady,dis);
		}
		
		if(best!=1)
		{
		if(right)
		{
			if(sumx<0 || Math.abs(sumy)>Math.abs(sumx))
				{
					if(sumy>0 && counter[2]==best)
					{
						up=true;
						right=false;
					}
					else if(counter[4]==best)
					{
						down=true;
						right=false;
					}
				}
		}
		else if(left)
		{
			if(sumx>0 || Math.abs(sumy)>Math.abs(sumx))
			{

				if(sumy>0 && counter[2]==best)
				{
					up=true;
					left=false;
				}
				else if(counter[4]==best)
				{
					down=true;
					left=false;
				}
			}
		}
		else if(up)
		{
			if(sumy<0 || Math.abs(sumy)<Math.abs(sumx))
			{

				if(sumx>0 && counter[3]==best)
				{
					right=true;
					up=false;
				}
				else if(counter[5]==best)
				{
					left=true;
					up=false;
				}
			}
		}
		else if(down)
		{
			if(sumy>0 || Math.abs(sumy)<Math.abs(sumx))
			{

				if(sumx>0 && counter[3]==best)
				{
					right=true;
					down=false;
				}
				else if(counter[5]==best)
				{
					left=true;
					down=false;
				}
			}
		}
		}
		
	}
	
	public void paint(Graphics g)
	{
		
		if(moves==0)
		{
			snakexlength[2]=50;
			snakexlength[1]=75;
			snakexlength[0]=100;
			
			snakeylength[2]=100;
			snakeylength[1]=100;
			snakeylength[0]=100;
		}
		
		
		g.setColor(Color.white);
		g.drawRect(24,10,851,55);
		
		titleImage=new ImageIcon("snaketitle.jpg");
		titleImage.paintIcon(this, g, 25, 11);
		
		g.setColor(Color.white);
		g.drawRect(24, 74, 851, 577);
		
		g.setColor(Color.BLACK);
		g.fillRect(25,75,850,575);
		
		g.setColor(Color.white);
		g.setFont(new Font("arial",Font.PLAIN,14));
		g.drawString("Score: "+score, 780, 30);
		
		g.setColor(Color.white);
		g.setFont(new Font("arial",Font.PLAIN,14));
		g.drawString("Length: "+lengthofsnake, 780, 50);
		
		
		
		rightmouth=new ImageIcon("rightmouth.png");
		rightmouth.paintIcon(this, g, snakexlength[0], snakeylength[0]);
		
		for(int a=0;a<lengthofsnake;a++)
		{
			if(a==0 && right)
			{
				rightmouth=new ImageIcon("rightmouth.png");
				rightmouth.paintIcon(this, g, snakexlength[a], snakeylength[a]);
				
			}
			
			if(a==0 && left)
			{
				leftmouth=new ImageIcon("leftmouth.png");
				leftmouth.paintIcon(this, g, snakexlength[a], snakeylength[a]);
				
			}
			
			if(a==0 && down)
			{
				downmouth=new ImageIcon("downmouth.png");
				downmouth.paintIcon(this, g, snakexlength[a], snakeylength[a]);
				
			}
			
			if(a==0 && up)
			{
				upmouth=new ImageIcon("upmouth.png");
				upmouth.paintIcon(this, g, snakexlength[a], snakeylength[a]);
				
			}
			
			if(a!=0)
			{
				snakeimage=new ImageIcon("snakeimage.png");
				snakeimage.paintIcon(this, g, snakexlength[a], snakeylength[a]);
				
			}
			
			
			
		}
		
		enemyimage=new ImageIcon("enemy.png");
		
		if(enemyxpos[xpos]==snakexlength[0] && enemyypos[ypos]==snakeylength[0])
		{
			score=score+5;
			lengthofsnake++;
			xpos=random_generator();
			ypos=xpos/34;
			ypos=22-ypos;
			xpos=xpos%34;
		}
		
		enemyimage.paintIcon(this, g, enemyxpos[xpos], enemyypos[ypos]);
		
		for(int b=1;b<lengthofsnake;b++)
		{
			if(snakexlength[b]==snakexlength[0] && snakeylength[b]==snakeylength[0])
			{
				right=false;
				left=false;
				up=false;
				down=false;
				g.setColor(Color.white);
				g.setFont(new Font("arial",Font.BOLD,50));
				g.drawString("Game Over", 300, 300);
				
				g.setColor(Color.white);
				g.setFont(new Font("arial",Font.BOLD,20));
				g.drawString("Press ESC to RESTART", 325, 340);
				running=false;
				end=true;
			}
		}
		
		if(!running && !end)
		{
			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.BOLD,50));
			g.drawString("Game Paused", 280, 300);
			
			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.BOLD,20));
			g.drawString("Press SPACE to RESUME", 325, 340);
			
		}
		
		if(moves==0)
		{

			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.BOLD,25));
			g.drawString("Press any ARROW key to START", 285, 340);
			
		}
		
		if(automatic)
		{
			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.BOLD,14));
			g.drawString("AUTOMATIC", 75, 30);
			
			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.PLAIN,14));
			g.drawString("Press F5 for MANUAL", 50, 50);
			
		}
		else
		{
			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.BOLD,14));
			g.drawString("MANUAL", 97, 30);
			
			g.setColor(Color.white);
			g.setFont(new Font("arial",Font.PLAIN,14));
			g.drawString("Press F5 for AUTOMATIC", 50, 50);
			
		}
		
		g.dispose();
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		
		timer.start();
		if(automatic && running)
		{
			update();
			repaint();
		}
		
		
		if(right && running)
		{
			for(int r=lengthofsnake;r>=0;r--)
			{
				snakeylength[r+1]=snakeylength[r];
			}
			
			for(int r=lengthofsnake;r>=0;r--)
			{
				if(r==0)
				{
					snakexlength[r]=snakexlength[r]+25;
				}
				else
				{
					snakexlength[r]=snakexlength[r-1];
				}
				if(snakexlength[r]>850)
				{
					snakexlength[r]=25;
				}
			}

			repaint();
		}
		
		if(left && running)
		{
			for(int r=lengthofsnake;r>=0;r--)
			{
				snakeylength[r+1]=snakeylength[r];
			}
			
			for(int r=lengthofsnake;r>=0;r--)
			{
				if(r==0)
				{
					snakexlength[r]=snakexlength[r]-25;
				}
				else
				{
					snakexlength[r]=snakexlength[r-1];
				}
				if(snakexlength[r]<25)
				{
					snakexlength[r]=850;
				}
			}

			repaint();
		}
		
		if(up && running)
		{
			for(int r=lengthofsnake;r>=0;r--)
			{
				snakexlength[r+1]=snakexlength[r];
			}
			
			for(int r=lengthofsnake;r>=0;r--)
			{
				if(r==0)
				{
					snakeylength[r]=snakeylength[r]-25;
				}
				else
				{
					snakeylength[r]=snakeylength[r-1];
				}
				if(snakeylength[r]<75)
				{
					snakeylength[r]=625;
				}
			}

			repaint();
		}
		
		if(down && running)
		{
			for(int r=lengthofsnake;r>=0;r--)
			{
				snakexlength[r+1]=snakexlength[r];
			}
			
			for(int r=lengthofsnake;r>=0;r--)
			{
				if(r==0)
				{
					snakeylength[r]=snakeylength[r]+25;
				}
				else
				{
					snakeylength[r]=snakeylength[r-1];
				}
				if(snakeylength[r]>625)
				{
					snakeylength[r]=75;
				}
			}

			repaint();
		}
		
	}
 
	@Override
	public void keyPressed(KeyEvent e) {
		
		if(e.getKeyCode()==KeyEvent.VK_F5)
		{
			if(automatic)
				automatic=false;
			else
				automatic=true;
			repaint();
		}
		
		if(e.getKeyCode()==KeyEvent.VK_ESCAPE)
		{
			right=false;
			left=false;
			down=false;
			up=false;
			running=true;
			end=false;
			moves=0;
			score=0;
			lengthofsnake=3;
			repaint();
		}
		
		if(e.getKeyCode()==KeyEvent.VK_SPACE && moves!=0)
		{
			if(running)
				running=false;
			else
				running=true;
			repaint();
		}
		
		if(e.getKeyCode()==KeyEvent.VK_RIGHT && running)
		{
			moves++;
			if(!left)
			{
				right=true;
				left=false;
			}
			else 
			{
				right=false;
				left=true;
			}
			up=false;
			down=false;
			
		}
		
		if(e.getKeyCode()==KeyEvent.VK_LEFT && running)
		{
			moves++;
			if(!right)
			{
				right=false;
				left=true;
			}
			else 
			{
				right=true;
				left=false;
			}
			
			up=false;
			down=false;
			
		}
		
		if(e.getKeyCode()==KeyEvent.VK_UP && running)
		{
			moves++;
			if(!down)
			{
				down=false;
				up=true;
			}
			else 
			{
				down=true;
				up=false;
			}
			
			right=false;
			left=false;
			
		}
		
		if(e.getKeyCode()==KeyEvent.VK_DOWN && running)
		{
			moves++;
			if(!up)
			{
				up=false;
				down=true;
			}
			else 
			{
				up=true;
				down=false;
			}
			
			right=false;
			left=false;
			
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
}
