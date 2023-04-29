/*
    Chess Pieces
 -------------------
   0: BlackRook1
   1: BlackKnight1
   2: BlackBishop1
   3: BlackQueen
   4: BlackKing
   5: BlackBishop2
   6: BlackKnight2
   7: BlackRook2
   8: BlackPawn1
   9: BlackPawn2
   10: BlackPawn3
   11: BlackPawn3
   12: BlackPawn4
   13: BlackPawn5
   14: BlackPawn6
   15: BlackPawn7
   
   16: WhitePawn1
   17: WhitePawn2
   18: WhitePawn3
   19: WhitePawn3
   20: WhitePawn4
   21: WhitePawn5
   22: WhitePawn6
   23: WhitePawn7
   24: WhiteRook1
   25: WhiteKnight1
   26: WhiteBishop1
   27: WhiteQueen
   28: WhiteKing
   29: WhiteBishop2
   30: WhiteKnight2
   31: WhiteRook2
   
   */
import java.io.*;
public class Board
{
    long piece[]=new long[32];
    int designation[]=new int[32];
    long whitePos;
    long blackPos;
    double weight;
    int collision;
    long states;
    long black_king_legal=-1;
    int piece_moved;
    final double king_value=10000000;
    final double inf=99999999;
    
    char rep[]={'E','H','B','Q','K','B','H','E','P','P','P','P','P','P','P','P','p','p','p','p','p','p','p','p','e','h','b','q','k','b','h','e'};
	//characters to represent the board during debugging using displayBoard function
    Board()//Unparamatarised constructor to create a board object
    {
       for(int i=0;i<32;i++)
        {
    	   piece[i]=0;
    	   designation[i]=i;
        }
        weight=0;
        collision=0;
        states=0;
        piece_moved=-1;
        black_king_legal=-1;
    }
    
    void reset()//method to reset the board positions to a new game
    {
        for(int i=0;i<16;i++)
        {
         piece[i]=((long)1)<<(63-i);
        }
        
        for(int i=16;i<32;i++)
        {
         piece[i]=((long)1)<<(31-i);
        }
        weight=0;
        collision=0;
        states=0;
        piece_moved=-1;
        black_king_legal=-1;
        whiteComponents();
        blackComponents();
    }
    
    
    Board(long p[],int des[])//parameterised constructor to create a board with respect to given parameters
    {
        for(int i=0;i<32;i++)
        {
            piece[i]=p[i];
            designation[i]=des[i];
        }
        collision=0;
        states=0;
        weight=0;
        piece_moved=-1;
        black_king_legal=-1;
        whiteComponents();
        blackComponents();
    }
    
    void displayBoard()//method to display board state in console for debugging purposes
    {
        String board="...........................................................................";
        
        for(int i=0;i<32;i++)
        {
          if(piece[i]!=0)
          {
            String s=Long.toBinaryString(piece[i]);
            int loc=64-s.length();
            board=board.substring(0,loc)+rep[designation[i]]+board.substring(loc+1);
          }
        }
        System.out.println("------BOARD------");
        for(int i=0;i<8;i++)
        {
            for(int j=0;j<8;j++)
            {
                System.out.print(" "+board.charAt(i*8+j));
            }
            System.out.println();
        }
        System.out.println("-----------------");
    }
    
    void bitBoard(Long n)//bitboard representation of the position/legal moves of a piece given its long representation
    {
        String s=Long.toBinaryString(n);
        while(s.length()<64)
        s="0"+s;
        System.out.println("------BOARD------");
        for(int i=0;i<8;i++)
        {
            for(int j=0;j<8;j++)
            {
                System.out.print(" "+s.charAt(i*8+j));
            }
            System.out.println();
        }
        System.out.println("-----------------");
    }
    
    void evaluate(int choice)//method to evaluate the value of the current state of the board
    {//a lower value is favorable to the black piece and a high value is favorable to white piece
     double value[]={-7,-6,-5,-9,(-king_value/100),-5,-6,-7,-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,7,6,5,9,(king_value/100),5,6,7};
     //value a chess piece contributes given it is present in a certain board state
	 double result=0;
     for(int i=0;i<32;i++)//for each of the 32 pieces
     {
         if(piece[i]!=0)//if present on board ie. alive
         {
             result+=(value[designation[i]]*100);//result is determined by the value of the piece remaining on the board
             	int loc=Long.numberOfLeadingZeros(piece[i]);
				int x=loc/8;//present row of the piece
				int y=loc%8;//present col of the piece
				int distance=0;
				int index=designation[i];
				if(index>=8 && index<16)
					distance=7-x;// the best position of the black pawn is to be at the last row of the chess board
				else if(index>=16 && index<24)
					distance=x;// the best position of the white pawn is to be at the first row of the chess board
				else if(index==4)//the best position for the black king is to be either at the
					distance=Math.min((x+y),(x+Math.abs(y-7)));//top left or the top right corner of the board
				else if(index==28)//the best position for the white king is to be either at the down most 
					distance=Math.min((Math.abs(x-7)+y),(Math.abs(x-7)+Math.abs(y-7)));//right or left corner of the board
				else if(index==0)//the best position of the leftmost black rook is to be at the left most column
					distance=Math.abs(y-7);
				else if(index==7)//the best position of the righmost black rook is to be at the top most row
					distance=Math.abs(x-7);
				else if(index==24)//the best position of the leftmost white rook is to be at the right most column
					distance=Math.abs(y-7);
				else if(index==31)//the best positions of the rightmost white rook is to be at the down most column
					distance=x;
				else// for the remaining pieces ie. queen, knight & bishop the best position is to be at the centre of the board
				{
					distance=Math.min((Math.abs(x-3)+Math.abs(y-3)),(Math.abs(x-3)+Math.abs(y-4)));
					distance=Math.min(distance,(Math.abs(x-4)+Math.abs(y-3)));
					distance=Math.min(distance,(Math.abs(x-4)+Math.abs(y-4)));
				}
				//distance corresponds to how far is a particular piece from its best position of attack/defend
				//the lower the distance the better is the piece located and the more favorable for its king
				if(index<16)
					result+=distance;
				else
					result-=distance;
					
	     }
     }
     
     if(piece[4]==0)//if the black king is killed the result increases tremendously in white's favour
    	 result+=(king_value);
     else if(piece[28]==0)//if the white king is killed the result decreses tremendously in black's favour
    	 result-=(king_value);
     
     this.weight=result;//the final weight of the board is returned to the calling object
	 
    }
    
    void blackComponents()//bitwise long representation of the positions of the black pieces in present board state
    {
        long val=0;
        for(int i=0;i<16;i++)
        {
            val=val|piece[i];
        }
        blackPos=val;
    }
    
    void whiteComponents()//bitwise long representation of the positions of the white pieces in present board state
    {
        long val=0;
        for(int i=16;i<32;i++)
        {
            val=val|piece[i];
        }
        whitePos=val;
    }
    
    Board moves(int index,int move)//this method returns the new board state after a piece is moved to its new position
    {	//bitwise shift operation is used to move a piece to its new position
		//positive move means right shift and negative means left shift
		//index denotes piece index
        Board ref=this;
        if(move>0)
        {
            piece[index]=piece[index]>>>move;
        }
        else if(move<0)
        {
            move=-move;
            piece[index]=piece[index]<<move;
        }
        
        
        if(index<16)
        {
            if((piece[index]&blackPos)!=0)//if a black piece tries to move to a location already 
            {			//occupied by another black piece then this move is illegal and null is returned
                return null;
            }
            else if((piece[index]&whitePos)!=0)//if a black piece tries to move to a location already
            {			//occupied by a white piece then it will replace the white piece
                for(int i=16;i<32;i++)//16-31 are white pieces
                {
                    if((piece[i]&piece[index])!=0)//the white piece which it replaces
                    {
                        piece[i]=0;//is set to 0 ie. removed from the board
                        break;
                    }
                }
                collision=1;// flag to represent that a collision has occured
            }
            
        }
        else
        {
            if((piece[index]&whitePos)!=0)//if a white piece tries to move to a location already
             return null;// occupied by another white piece then this move is illegal and null is returned
            else if((piece[index]&blackPos)!=0)//if a white piece tries to move to a location already 
            {// occupied by a black piece then it will replace the black piece
                for(int i=0;i<16;i++)//0-15 are black pieces
                {
                    if((piece[i]&piece[index])!=0)//the black piece which it replaces
                    {
                        piece[i]=0;//is set to 0 ie. removed from the board
                        break;
                    }
                }
                collision=1;//flag to represent that a collision has occured
            }
            
        }
        return ref;//return the new board state  
    }
    
   
   
  
    Board rook(int i,int choice,int depth,double alpha,double beta)//returns the best rook move possible for piece index i 
    {
        int loc=63-Long.numberOfLeadingZeros(piece[i]);
        int up=7-(loc/8);//no of moves possible towards the top
        int down=(loc/8);//no of moves possible in the downwards direction
        int right=(loc%8);//no of moves possible towards the right
        int left=7-(loc%8);//no of moves possible towards the left 
        long legal_states=0;
        Board min=null;
        Board b=new Board(piece,designation);
        for(int j=0;j<right;j++)//for all the positions the rook can move to its right
        {
            b=new Board(b.piece,b.designation);
            b=b.moves(i,1);
            if(b==null)//denotes no further legal moves to the right
            break;
            
			if(depth==0)
            b.evaluate(choice);//evaluate the chess board value at the leaf node of the minimax tree
			else 
			{
				//if leaf node is not reached find the value of the best move recursively down the minimax tree
				b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
			}											 			  

            if(min==null || (min.weight*choice)>(b.weight*choice))//if this position of rook yields the most favorable 
            min=b;//                                              board value, then this new board state is stored in min

        	if(depth!=1 || choice*b.weight<(king_value/2))//At depth 1, the next level depth 0 is for evaluation. So all moves
            legal_states|=b.piece[i];//at depth 1 are legal. For other depth the move is legal only if the black King is safe
            if(b.collision==1)//if the black rook's position coincides with a white piece ie. collision has occured, then 
            break;//            further move to the right is not possible
        }
        b=new Board(piece,designation);
        for(int j=0;j<left;j++)//for all the positions the rook can move to its left
        {
            b=new Board(b.piece,b.designation);
            b=b.moves(i,-1);
            if(b==null)//denotes no further legal moves to the left
            break;
            
			if(depth==0)
	            b.evaluate(choice);//evaluate the chess board value at the leaf node of the minimax tree 
			else 
			{
				//if leaf node is not reached find the value of the best move recursively down the minimax tree 
				b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
			}

            if(min==null || (min.weight*choice)>(b.weight*choice))//if this position of rook yields the most favorable 
            min=b;//											   board value, then this new board state is stored in min 					

        	if(depth!=1 || choice*b.weight<(king_value/2))//At depth 1, the next level depth 0 is for evaluation. So all moves
            legal_states|=b.piece[i];//at depth 1 are legal. For other depth the move is legal only if the black King is safe
            if(b.collision==1)//if the black rook's position coincides with a white piece ie. collision has occured, then 
            break;//            further move to the left is not possible
        }
        
        b=new Board(piece,designation);
        for(int j=0;j<up;j++)//for all the positions the rook can move up
        {
            b=new Board(b.piece,b.designation);
            b=b.moves(i,-8);
            if(b==null)
            break;
            
            if(depth==0)
                b.evaluate(choice);
			else 
			{
				b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
			}

            if(min==null || (min.weight*choice)>(b.weight*choice))
            min=b;

        	if(depth!=1 || choice*b.weight<(king_value/2))
            legal_states|=b.piece[i];
            if(b.collision==1)
            break;
        }
        
        b=new Board(piece,designation);
        for(int j=0;j<down;j++)//for all the positions the rook can move down
        {
            b=new Board(b.piece,b.designation);
            b=b.moves(i,8);
            if(b==null)
            break;
            
            if(depth==0)
                b.evaluate(choice);
			else 
			{
				b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
			}

            if(min==null || (min.weight*choice)>(b.weight*choice))
            min=b;

        	if(depth!=1 || choice*b.weight<(king_value/2))
            legal_states|=b.piece[i];
            if(b.collision==1)
            break;
        }
		if(min!=null)//if there is a valid position available for the rook to move 
        {
			min.states=legal_states;//legal positions the moved chess piece could have taken
			min.piece_moved=i;//index of the chess piece moved
        }
        return min;// return the most favourable chess board state
    }
    
    Board bishop(int i,int choice,int depth,double alpha,double beta)//returns the best bishop move possible for piece index i
    {
        int loc=63-Long.numberOfLeadingZeros(piece[i]);
        int up=7-(loc/8);
        int down=(loc/8);
        int right=(loc%8);
        int left=7-(loc%8);
        long legal_states=0;
		Board min=null;

        Board b=new Board(piece,designation);
        for(int j=0;j<Math.min(right,down);j++)//for all positions to the down-right diagonal
        {
            b=new Board(b.piece,b.designation);
            b=b.moves(i,9);
            if(b==null)
            break;
        	
			if(depth==0)
	            b.evaluate(choice);
			else 
			{
				b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
			}

            if(min==null || (min.weight*choice)>(b.weight*choice))
            min=b;

        	if(depth!=1 || choice*b.weight<(king_value/2))
            legal_states|=b.piece[i];
            if(b.collision==1)
            break;
        }
        b=new Board(piece,designation);
        for(int j=0;j<Math.min(right,up);j++)//for all positions to the up-right diagonal
        {
            b=new Board(b.piece,b.designation);
            b=b.moves(i,-7);
            if(b==null)
            break;
         	
			if(depth==0)
	            b.evaluate(choice);
			else 
			{
				b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
			}

            if(min==null || (min.weight*choice)>(b.weight*choice))
            min=b;

        	if(depth!=1 || choice*b.weight<(king_value/2))
            legal_states|=b.piece[i];
            if(b.collision==1)
            break;
        }
        
        b=new Board(piece,designation);
        for(int j=0;j<Math.min(left,down);j++)//for all positions to the down-left diagonal 
        {
            b=new Board(b.piece,b.designation);
            b=b.moves(i,7);
            if(b==null)
            break;
        	
			if(depth==0)
            b.evaluate(choice);
			else 
			{
				b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
			}

            if(min==null || (min.weight*choice)>(b.weight*choice))
            min=b;

        	if(depth!=1 || choice*b.weight<(king_value/2))
            legal_states|=b.piece[i];
            if(b.collision==1)
            break;
        }
        
        b=new Board(piece,designation);
        for(int j=0;j<Math.min(left,up);j++)//for all positions to the up-left diagonal 
        {
            b=new Board(b.piece,b.designation);
            b=b.moves(i,-9);
            if(b==null)
            break;
         	
			if(depth==0)
            b.evaluate(choice);
			else 
			{
				b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
			}

            if(min==null || (min.weight*choice)>(b.weight*choice))
            min=b;

        	if(depth!=1 || choice*b.weight<(king_value/2))
            legal_states|=b.piece[i];
            if(b.collision==1)
            break;
        }
        if(min!=null)
        {
			min.states=legal_states;
			min.piece_moved=i;
        }
        return min;
    }
    
    
    Board knight(int i,int choice,int depth,double alpha,double beta)//returns the best knight move possible for piece index i
    {
        int loc=63-Long.numberOfLeadingZeros(piece[i]);
        int up=7-(loc/8);
        int down=(loc/8);
        int right=(loc%8);
        int left=7-(loc%8);
        long legal_states=0;
		Board min=null;

        Board b=new Board(piece,designation);
        if(right>=1 && up>=2)
        {
            b=b.moves(i,-15);
            if(b!=null)
            {
            
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(right>=2 && up>=1)
        {
            b=b.moves(i,-6);
            if(b!=null)
            {
            
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
       
        b=new Board(piece,designation);
        if(right>=2 && down>=1)
        {
            b=b.moves(i,10);
            if(b!=null)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(right>=1 && down>=2)
        {
            b=b.moves(i,17);
            if(b!=null)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(left>=1 && down>=2)
        {
            b=b.moves(i,15);
            if(b!=null)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }        
        }
        
        b=new Board(piece,designation);
        if(left>=2 && down>=1)
        {
            b=b.moves(i,6);
            if(b!=null)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(left>=2 && up>=1)
        {
            b=b.moves(i,-10);
            if(b!=null)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(left>=1 && up>=2)
        {
            b=b.moves(i,-17);
            if(b!=null)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        if(min!=null)
        {
			min.states=legal_states;
			min.piece_moved=i;
        }
        
        return min;
    }
    
    Board queen(int i,int choice,int depth,double alpha,double beta)//returns the best queen move possible for piece index i
    {//                                     A queen's move is basically the combination of the moves of rook and bishop 
        long legal_states=0;
        Board b=new Board(piece,designation);
		Board min=null;
        min=b.rook(i,choice,depth,alpha,beta);//the best move if the queen moved as a rook
		
		if(min!=null)
		legal_states|=min.states;
		
		b=b.bishop(i,choice,depth,alpha,beta);//the best move if the queen moved as a bishop 
		
		if(b!=null)
		legal_states|=b.states;
		
		if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
        min=b;
		
		if(min!=null)
        {
			min.states=legal_states;
			min.piece_moved=i;
        }
		
        return min;// the best of all legal board states 
    }
    
    Board king(int i,int choice,int depth,long legal,double alpha,double beta)//returns the best king move possible for piece index i
    {
        int loc=63-Long.numberOfLeadingZeros(piece[i]);
        int up=7-(loc/8);
        int down=(loc/8);
        int right=(loc%8);
        int left=7-(loc%8);
        long legal_states=0;
		Board min=null;
        Board b=new Board(piece,designation);
        if(right>=1)
        {
            b=b.moves(i,1);
            if(b!=null && (b.piece[i]&legal)!=0)//legal corresponds to all the legal moves the king can take 
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;
            	
            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(down>=1)
        {
            b=b.moves(i,8);
            if(b!=null && (b.piece[i]&legal)!=0)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
       
        b=new Board(piece,designation);
        if(left>=1)
        {
            b=b.moves(i,-1);
            if(b!=null && (b.piece[i]&legal)!=0)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(up>=1)
        {
            b=b.moves(i,-8);
            if(b!=null && (b.piece[i]&legal)!=0)
            {
			
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(right>=1 && up>=1)
        {
            b=b.moves(i,-7);
            if(b!=null && (b.piece[i]&legal)!=0)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }        
        }
        
        b=new Board(piece,designation);
        if(right>=1 && down>=1)
        {
            b=b.moves(i,9);
            if(b!=null && (b.piece[i]&legal)!=0)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(left>=1 && down>=1)
        {
            b=b.moves(i,7);
            if(b!=null && (b.piece[i]&legal)!=0)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        
        b=new Board(piece,designation);
        if(left>=1 && up>=1)
        {
            b=b.moves(i,-9);
            if(b!=null && (b.piece[i]&legal)!=0)
            {
             
				if(depth==0)
            	b.evaluate(choice);
				else 
				{
				   b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
				}

            	if(min==null || (min.weight*choice)>(b.weight*choice))
            	min=b;

            	if(depth!=1 || choice*b.weight<(king_value/2))
                legal_states|=b.piece[i];
            }
        }
        if(min!=null)
        {
			min.states=legal_states;
			min.piece_moved=i;
        }
        return min;
    }
    
    
    Board pawn(int i,int choice,int depth,double alpha,double beta)//returns the best pawn move possible for piece index i
    {
        int loc=63-Long.numberOfLeadingZeros(piece[i]);
        int up=7-(loc/8);
        int down=(loc/8);
        int right=(loc%8);
        int left=7-(loc%8);
        long legal_states=0;
		Board min=null;
        if(i<16)// if it is a black pawn 
        {
            Board b=new Board(piece,designation);
            if(down>=1)
            {
                b.piece[i]>>>=8;
                	
                if((b.piece[i]&(b.blackPos|b.whitePos))!=0)//pawn cannot move forward if the place is already occupied 
                {//                                     			by any other chess piece, be it black/white
                    b=null;
                }
                else
                {
                	
                    if(loc>=8 && loc<16)//if the black pawn has not moved yet, then it is as valuable as a black queen 
                    	b.designation[i]=3;// since it acts as a defence for the king (black queen's index=3)
			
					if(depth==0)
            		b.evaluate(choice);
					else 
					{
				   		b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
					}

            		if(min==null || (min.weight*choice)>(b.weight*choice))
            		min=b;

                	if(depth!=1 || choice*b.weight<(king_value/2))
                    legal_states|=b.piece[i];
                }
            }
            
            if(up==1 && legal_states!=0)//if black pawn has not moved yet and it can legally take two steps without obstruction
            {
                b=new Board(piece,designation);
                b.piece[i]>>>=16;
                if((b.piece[i]&(b.blackPos|b.whitePos))!=0)
                {
                    b=null;
                }
                else
                {
             
					if(depth==0)
            		b.evaluate(choice);
					else 
					{
				   		b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
					}

            		if(min==null || (min.weight*choice)>(b.weight*choice))
            		min=b;

                	if(depth!=1 || choice*b.weight<(king_value/2))
                    legal_states|=b.piece[i];
                }
            }
            
            if(down>=1 && right>=1)
            {
                b=new Board(piece,designation);
                b.piece[i]>>>=9;
                if((b.piece[i]&(b.blackPos|(~b.whitePos)))!=0)//diagonal movement allows pawn to replace its opponent's piece
                {
                    b=null;
                }
                else
                { 
					for(int index=16;index<32;index++)//16-31 are white pieces
                	{
						if((b.piece[i]&b.piece[index])!=0)
                    	{
                        	b.piece[index]=0;
                        	break;
                    	}
                	}
             		

                    if(loc>=8 && loc<16)
                    	b.designation[i]=3;
			
					if(depth==0)
            		b.evaluate(choice);
					else 
					{
				   		b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
					}

            		if(min==null || (min.weight*choice)>(b.weight*choice))
            		min=b;

                	if(depth!=1 || choice*b.weight<(king_value/2))
                    legal_states|=b.piece[i];
                }
            }
            
            if(down>=1 && left>=1)
            {
                b=new Board(piece,designation);
                b.piece[i]>>>=7;
                if((b.piece[i]&(b.blackPos|(~b.whitePos)))!=0)
                {
                    b=null;
                }
                else
                {
					for(int index=16;index<32;index++)//16-31 are white pieces
                	{
                    	if((b.piece[i]&b.piece[index])!=0)
                    	{
                        	b.piece[index]=0;
                        	break;
                    	}
                	}
                    if(loc>=8 && loc<16)
                    	b.designation[i]=3;
			
					if(depth==0)
            		b.evaluate(choice);
					else 
					{
				   		b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
					}

            		if(min==null || (min.weight*choice)>(b.weight*choice))
            		min=b;

                	if(depth!=1 || choice*b.weight<(king_value/2))
                    legal_states|=b.piece[i];
                }
            }
            
            
        }
        else// if it is a white pawn 
        {
            Board b=new Board(piece,designation);
            if(up>=1)
            {
                b.piece[i]<<=8;
                if((b.piece[i]&(b.blackPos|b.whitePos))!=0)
                {
                    b=null;
                }
                else
                {
             
                    if(loc>=48 && loc<56)//if the white pawn has not moved yet, then it is as valuable as a white queen 
                    	b.designation[i]=27;// since it acts as a defence for the king (white queen's index=27)
			
					if(depth==0)
            		b.evaluate(choice);
					else 
					{
				   		b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
					}

            		if(min==null || (min.weight*choice)>(b.weight*choice))
            		min=b;

                	if(depth!=1 || choice*b.weight<(king_value/2))
                    legal_states|=b.piece[i];
                }
            }
            
            if(down==1 && legal_states!=0)
            {
                b=new Board(piece,designation);
                b.piece[i]<<=16;
                if((b.piece[i]&(b.blackPos|b.whitePos))!=0)
                {
                    b=null;
                }
                else
                {
             
					if(depth==0)
            		b.evaluate(choice);
					else 
					{
				   		b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
					}

            		if(min==null || (min.weight*choice)>(b.weight*choice))
            		min=b;

                	if(depth!=1 || choice*b.weight<(king_value/2))
                    legal_states|=b.piece[i];
                }
            }
            
            if(up>=1 && right>=1)
            {
                b=new Board(piece,designation);
                b.piece[i]<<=7;
                if((b.piece[i]&(b.whitePos|(~b.blackPos)))!=0)
                {
                    b=null;
                }
                else
                {
					for(int index=0;index<16;index++)//16-31 are black pieces
                	{
                    	if((b.piece[i]&b.piece[index])!=0)
                    	{
                        	b.piece[index]=0;
                        	break;
                    	}
                	}
             		
                    if(loc>=48 && loc<56)
                    	b.designation[i]=27;
			
					if(depth==0)
            		b.evaluate(choice);
					else 
					{
				   		b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
					}

            		if(min==null || (min.weight*choice)>(b.weight*choice))
            		min=b;

                	if(depth!=1 || choice*b.weight<(king_value/2))
                    legal_states|=b.piece[i];
                }
            }
            
            if(up>=1 && left>=1)
            {
                b=new Board(piece,designation);
                b.piece[i]<<=9;
                if((b.piece[i]&(b.whitePos|(~b.blackPos)))!=0)
                {
                    b=null;
                }
                else
                {
					for(int index=0;index<16;index++)//16-31 are black pieces
                	{
                    	if((b.piece[i]&b.piece[index])!=0)
                    	{
                        	b.piece[index]=0;
                        	break;
                    	}
                	}
             		
                    if(loc>=48 && loc<56)
                    	b.designation[i]=27;
			
					if(depth==0)
            		b.evaluate(choice);
					else 
					{
				   		b.weight=(b.minimax(-choice,depth-1,alpha,beta)).weight;
					}

            		if(min==null || (min.weight*choice)>(b.weight*choice))
            		min=b;

                	if(depth!=1 || choice*b.weight<(king_value/2))
                    legal_states|=b.piece[i];
                }
            }
            
        }
        if(min!=null)
        {
			min.states=legal_states;
			min.piece_moved=i;
        }
        return min;
    }
    

	Board minimax(int choice,int depth,double alpha,double beta)
	{//method using minimax algorithm with alpha beta pruning to find the best move for a player given a chess board state
		Board obj=this;
		Board b=null;
		Board min=null;
		if(choice==1)//corresponds to black piece
		{
			int randomInt=((int)(100.0*Math.random()))%16;//to find the piece index whose best move is to calculated first
			for(int k=0;k<16;k++)
        	{
				int j=(randomInt+k)%16;
						
				int i=obj.designation[j];
				
				if(piece[j]==0)
					continue;
				
				if(min!=null)
				{
					if(beta>min.weight)
						beta=min.weight;//beta stores the maximum possible weight in the subtree
					if(alpha>=beta)//if alpha is greater than equal to beta than the corresponding subtree would not contribute
						break;//  to the decision taken for the next move, thus it is pruned 
				}
				
            	if(i==0 || i==7 || i==24 || i==31)
            	{
					b=obj.rook(j,choice,depth,alpha,beta);//finding best move for the rook 
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
            	else if(i==1 || i==6 || i==25 || i==30)
            	{
					b=obj.knight(j,choice,depth,alpha,beta);//finding best move for the knight 
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
            	else if(i==2 || i==5 || i==26 || i==29)
            	{
					b=obj.bishop(j,choice,depth,alpha,beta);//finding best move for the bishop 
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
            	else if(i==3 || i==27)
            	{
					b=obj.queen(j,choice,depth,alpha,beta);// finding best move for the queen 
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
            	else if(i==4 || i==28)
            	{
            			b=obj.king(j,choice,depth,obj.black_king_legal,alpha,beta);//finding best move for the king 
            			if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            				min=b;
				}
            	else if(i>=8 && i<24)
            	{
					b=obj.pawn(j,choice,depth,alpha,beta);//finding best move for the pawn 
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
        	}
		}
		else if(choice==-1)//corresponds to white piece
		{
			int randomInt=((int)(100.0*Math.random()))%16;
			for(int k=0;k<16;k++)
        	{
				int j=(randomInt+k)%16+16;
				
				int i=obj.designation[j];

				if(piece[j]==0)
					continue;
				
				if(min!=null)
				{
					if(alpha<min.weight)//alpha stores the minimum possible weight for the subtree 
						alpha=min.weight;
					if(alpha>=beta)
						break;
				}
				
            	if(i==0 || i==7 || i==24 || i==31)
            	{
					b=obj.rook(j,choice,depth,alpha,beta);
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
            	else if(i==1 || i==6 || i==25 || i==30)
            	{
					b=obj.knight(j,choice,depth,alpha,beta);
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
            	else if(i==2 || i==5 || i==26 || i==29)
            	{
					b=obj.bishop(j,choice,depth,alpha,beta);
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
            	else if(i==3 || i==27)
            	{
					b=obj.queen(j,choice,depth,alpha,beta);
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
            	else if(i==4 || i==28)
            	{
            			b=obj.king(j,choice,depth,-1,alpha,beta);
            			if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            				min=b;	
				}
            	else if(i>=8 && i<24)
            	{
					b=obj.pawn(j,choice,depth,alpha,beta);
					if(min==null || (b!=null && (min.weight*choice)>(b.weight*choice)))
            		min=b;
				}
        	}
		}
		if(min==null)
		{
			min=new Board(obj.piece,obj.designation);
			min.evaluate(0);
		}
		
		if(depth==3)
		{
			if(min.weight<(-min.king_value/2))//if the white king will always be eliminated for all possible moves
			{
				Board temp=obj.minimax(1,0,-inf,inf);
				if(temp!=null && temp.weight<(-temp.king_value/2))//if the white king is in check that is it will be eliminated even 
					min.weight=-2*temp.king_value;//if it doesn't move, then this is the best conclusion team black can bring about
				else//if the king is not in check, but unable to make any legal move, it results in stalemate
					min.weight=0;//which is not favorable for team black, hence value of this node is 0
			}	
		}
		
		return min;// the best next move for the team black/white calling this method   
    
}
}

