<<<<<<< HEAD
import java.io.*; 
=======
import java.io.*;
>>>>>>> f2bf69d... Signed Commit
public class Rubiks_cube
{
    char a[][][][]=new char[3][3][3][6];
    char buff[]=new char[12];
    char blockbuff[][]=new char[12][6];
    int clk[][]={{0,6,8,2,9,1,3,7,5,10},{9,0,6,8,2,10,1,3,7,5}};
    int seq[][][]={{{1,2,3,4,9},{9,1,2,3,4}},{{0,2,5,4,9},{9,0,2,5,4}},{{0,1,5,3,9},{9,0,1,5,3}}};
    int row=-1,col=-1,layer=-1,sequence=-1;
    String decode[]={"F","U","L","R","B","D","X","Y","Z","f","u","l","r","b","d","x","y","z"};
    String encode[]={"F","U","LLL","R","BBB","DDD","RVL","UHD","FSB","FFF","UUU","L","RRR","B","D","RVLRVLRVL","UHDUHDUHD","FSBFSBFSB"};
    String move[]={"","",""};
    String ins[]={"Front","Top  ","Left ","Right","Back ","Down ","Cube Spin Right","Cube Spin Top  ","Cube Spin Front"};
    char instruct[]={'f','u','l','r','b','d','x','y','z'};
    int part=0;
    public void ini()
    {
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                for(int k=0;k<3;k++)
                {
                    for(int l=0;l<6;l++)
                    {
                        a[i][j][k][l]='V';
                    }
                }
            }
        }
        for(int i=0;i<12;i++)
        {
        buff[i]='V';
        for(int j=0;j<6;j++)
        {
            blockbuff[i][j]='V';
        }
        }
    }
    public void input(String s)
    {
        int n=0;
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                a[i][j][0][2]=s.charAt(n);
                n++;
            }
        }
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                buff[i*3+j]=s.charAt(n);
                n++;
            }
        }
        for(int i=0;i<10;i++)//clockwise rotation of buffer
        {
            buff[clk[1][i]]=buff[clk[0][i]];
        }
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                a[0][i][j][0]=buff[i*3+j];
            }
        }
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                a[i][0][2-j][1]=s.charAt(n);
                n++;
            }
        }
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                a[i][2][j][3]=s.charAt(n);
                n++;
            }
        }
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                a[i][2-j][2][4]=s.charAt(n);
                n++;
            }
        }
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                a[2][j][i][5]=s.charAt(n);
                n++;
            }
        }
        
    }
   
    public void display()
    {
        System.out.println("Front Face");
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                System.out.print(a[i][j][0][2]+" ");
            }
            System.out.println();
        }
        System.out.println("Upper Face");
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                buff[i*3+j]=a[0][i][j][0];
            }
        }
        for(int i=9;i>=0;i--)//anticlockwise rotation of buffer
        {
            buff[clk[0][i]]=buff[clk[1][i]];
        }
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                System.out.print(buff[i*3+j]+" ");
            }
            System.out.println();
        }
        System.out.println("Left Face");
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                System.out.print(a[i][0][2-j][1]+" ");
            }
            System.out.println();
        }
        System.out.println("Right Face");
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                System.out.print(a[i][2][j][3]+" ");
            }
            System.out.println();
        }
        System.out.println("Back Face");
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                System.out.print(a[i][2-j][2][4]+" ");
            }
            System.out.println();
        }
        System.out.println("Down Face");
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                System.out.print(a[2][j][i][5]+" ");
            }
            System.out.println();
        }
        
    }
    
    void evaluate(int r,int c,int l,int i)
    {
        if(r!=-1)
        {
            row=r;
            col=i/3;
            layer=i%3;
            sequence=0;
        }
        else if(c!=-1)
        {
            row=i/3;
            col=c;
            layer=i%3;
            sequence=1;
        }
        else if(l!=-1)
        {
            row=i/3;
            col=i%3;
            layer=l;
            sequence=2;
        }
    }
    
    public void rotate(int r,int c,int l) 
    {
        for(int i=0;i<9;i++)
        {
                evaluate(r,c,l,i);
                for(int k=0;k<6;k++)
                {
                    blockbuff[i][k]=a[row][col][layer][k];
                }
        }
        for(int i=0;i<10;i++)
        {
            for(int j=0;j<6;j++)
            {
                blockbuff[clk[1][i]][j]=blockbuff[clk[0][i]][j];
            }
        }
        for(int i=0;i<9;i++)
        {
            for(int j=0;j<6;j++)
            {
                buff[j]=blockbuff[i][j];
            }
            for(int j=0;j<5;j++)
            {
                buff[seq[sequence][1][j]]=buff[seq[sequence][0][j]];
            }
            for(int j=0;j<6;j++)
            {
                blockbuff[i][j]=buff[j];
            }
        }
        for(int i=0;i<9;i++)
        {
                evaluate(r,c,l,i);
                for(int k=0;k<6;k++)
                {
                    a[row][col][layer][k]=blockbuff[i][k];
                }
        }
      
    }
    
    public void decide(char ch)
    {
        switch(ch)
        {
            case 'F':row=-1;
            col=-1;
            layer=0;
            break;
            case 'U':row=0;
            col=-1;
            layer=-1;
            break;
            case 'L':row=-1;
            col=0;
            layer=-1;
            break;
            case 'R':row=-1;
            col=2;
            layer=-1;
            break;
            case 'B':row=-1;
            col=-1;
            layer=2;
            break;
            case 'D':row=2;
            col=-1;
            layer=-1;
            break;
            case 'V':row=-1;
            col=1;
            layer=-1;
            break;
            case 'H':row=1;
            col=-1;
            layer=-1;
            break;
            case 'S':row=-1;
            col=-1;
            layer=1;
            break;
        }
        rotate(row,col,layer);
    }
    
    
    public void execute(String s)
    {
        move[part]=move[part]+s;
        String ex="";
        for(int i=0;i<s.length();i++)
        {
            String s1=s.substring(i,i+1);
            for(int j=0;j<18;j++)
            {
                if(decode[j].compareTo(s1)==0)
                {
                    s1=encode[j];
                    break;
                }
            }
            ex=ex+s1;
        }
        for(int i=0;i<ex.length();i++)
        {
            decide(ex.charAt(i));
        }
        
    }
    
    
    public int layer_check(int r)
    {
        int p=1;
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
                if(a[r][i][j][0]!=a[r][1][1][0] || a[r][i][j][5]!=a[r][1][1][5])
                {
                    p=0;
                    break;
                }
            }
            if(p==0)
            break;
        }
        if(p==1)
        {
        for(int i=0;i<4;i++)
        {
            if(a[r][0][0][2]!=a[r][1][0][2] || a[r][2][0][2]!=a[r][1][0][2])
            {
                p=0;
            }
            rotate(r,-1,-1);
        }
        }
        return p;
    }
    
    public int cross_check()
    {
        int p=0;
        for(int i=0;i<4;i++)
        {
            if(a[2][1][0][2]==a[1][1][0][2])
            {
                p=1;
                for(int j=0;j<4;j++)
                {
                    if(a[2][1][0][2]!=a[1][1][0][2] || a[2][1][0][5]!=a[2][1][1][5])
                    p=0;
                    execute("Y");
                }
                
            }
            rotate(2,-1,-1);
        }
        return p;
    }
    
    public int daisy_count()
    {
        char colour=a[2][1][1][5];
        int count=0;
        if(a[0][1][0][0]==colour)
        count++;
        if(a[0][1][2][0]==colour)
        count++;
        if(a[0][0][1][0]==colour)
        count++;
        if(a[0][2][1][0]==colour)
        count++;
        return count;
    }
    
    public int orient()
    {
        int p=-1;
        for(int i=0;i<4;i++)
        {
            if(layer_check(2)==1)
            {
                p=0;
                break;
            }
            execute("X");
        }
        if(p==-1)
        {
        for(int i=0;i<4;i++)
        {
            if(layer_check(2)==1)
            {
                p=0;
                break;
            }
            execute("Z");
        }
        }
        
        if(p==-1)
        {
        for(int i=0;i<4;i++)
        {
            if(cross_check()==1)
            {
                p=1;
                break;
            }
            execute("X");
        }
        }
        
        if(p==-1)
        {
        for(int i=0;i<4;i++)
        {
            if(cross_check()==1)
            {
                p=1;
                break;
            }
            execute("Z");
        }
        }
        
        if(p==-1)
        {
            int max=daisy_count();
            char base=a[2][1][1][5];
            
        for(int i=0;i<4;i++)
        {
            int n=daisy_count();
            if(n==4)
            {
                p=2;
                break;
            }
            if(n>max)
            {
                max=n;
                base=a[2][1][1][5];
            }
            execute("X");
        }
        
        if(p==-1)
        {
            
        for(int i=0;i<4;i++)
        {
            int n=daisy_count();
            if(n==4)
            {
                p=2;
                break;
            }
            if(n>max)
            {
                max=n;
                base=a[2][1][1][5];
            }
            execute("Z");
        }
        }
        if(p!=2 && max>daisy_count())
        {
            for(int i=0;i<4;i++)
            {
                if(a[2][1][1][5]==base)
                {
                    p=3;
                    break;
                }
                execute("X");
            }
            
            if(p==-1)
            {
            for(int i=0;i<4;i++)
            {
                if(a[2][1][1][5]==base)
                {
                    p=3;
                    break;
                }
                execute("Z");
            }
            }
            
        }
        
        }
        
        
        if(p==0 || p==1)
        {
            while(a[1][1][0][2]!=a[2][1][0][2])
            execute("D");
        }
        
        return p;
    }
    
    
    public int daisy()
    {
        int p=0;
        if(daisy_count()!=4)
        {
            char colour=a[2][1][1][5];
            if(a[1][2][0][2]==colour || a[2][2][1][5]==colour || a[1][2][2][4]==colour)
            {
                while(a[0][2][1][0]==colour)
                execute("U");
                while(a[0][2][1][0]!=colour)
                execute("R");
            }
            else if(a[0][1][0][2]==colour)
            {
                execute("F");
                while(a[0][2][1][0]==colour)
                execute("U");
                execute("R");
            }
            else if(a[2][1][0][2]==colour)
            {
                while(a[0][1][0][0]==colour)
                execute("U");
                execute("f");
                while(a[0][2][1][0]==colour)
                execute("U");
                execute("R");
            }
            else
            execute("Y");
        }
        else
        p=1;
        return p;
    }
    
    public int cross()
    {
     int p=0;
     if(cross_check()!=1)
     {
         char colour=a[2][1][1][5];
         while(a[0][1][0][0]!=colour)
         execute("Y");
         while(a[0][1][0][2]!=a[1][1][0][2])
         execute("Yu");
         execute("FF");
     }
      else
      p=1;
     return p;
    }
    
    
    public int first_layer()
    {
        int p=0;
        if(layer_check(2)!=1)
        {
            int critical=0;
            char colour=a[2][1][1][5];
            for(int i=0;i<4;i++)
            {
                if(a[0][2][0][0]==colour || a[0][2][0][2]==colour || a[0][2][0][3]==colour)
                {
                    critical=1;
                    break;
                }
                execute("U");
            }
            while(critical==1)
            {
                char colour1=a[1][2][1][3];
                char colour2=a[1][1][0][2];
                char c1=a[0][2][0][0];
                char c2=a[0][2][0][2];
                char c3=a[0][2][0][3];
                if((c1==colour1 || c1==colour2 || c1==colour) && (c2==colour1 || c2==colour2 || c2==colour) && (c3==colour1 || c3==colour2 || c3==colour))
                break;
                execute("Yu");
            }
            if(critical==0)
            {
                for(int i=0;i<4;i++)
                {
                    if(a[2][2][0][2]!=a[1][1][0][2] || a[2][2][0][3]!=a[1][2][1][3] || a[2][2][0][5]!=a[2][1][1][5])
                    break;
                    execute("Yu");
                }
                char colour1=a[1][2][1][3];
                char colour2=a[1][1][0][2];
                char c1=a[2][2][0][2];
                char c2=a[2][2][0][5];
                char c3=a[2][2][0][3];
                if((c1==colour1 || c1==colour2 || c1==colour) && (c2==colour1 || c2==colour2 || c2==colour) && (c3==colour1 || c3==colour2 || c3==colour))
                critical=1;
            }
            do
            {
                execute("RUru");
            }
            while(critical==1 && (a[2][2][0][2]!=a[1][1][0][2] || a[2][2][0][3]!=a[1][2][1][3] || a[2][2][0][5]!=a[2][1][1][5]));   
        
        }
        else
        p=1;
        return p;
    }
    
    public int second_layer()
    {
        int p=0;
        if(part!=1)
            part=1;
        if(layer_check(1)!=1)
        {
            int found=0;
            for(int i=0;i<4;i++)
            {
                if(a[0][1][0][2]!=a[0][1][1][0] && a[0][1][0][0]!=a[0][1][1][0])
                {
                    found=1;
                    break;
                }
                execute("Y");
            }
            if(found==1)
            {
                while(a[0][1][0][2]!=a[1][1][0][2])
                execute("Yu");
                if(a[0][1][0][0]==a[1][2][1][3])
                execute("URurufUF");
                else if(a[0][1][0][0]==a[1][0][1][1])
                execute("ulULUFuf");
                
            }
            else 
            {
                for(int i=0;i<4;i++)
                {
                    if(a[1][2][0][2]!=a[1][1][0][2] || a[1][2][0][3]!=a[1][2][1][3])
                    {
                        execute("URurufUF");
                        break; 
                    }
                    execute("Y");
                }
            }
        }
        else
        p=1;
        return p;
    }
    
    public int upper_cross()
    {
        int p=0;
        if(part!=2)
            part=2;
        char colour=a[0][1][1][0];
        if(a[0][1][0][0]==colour && a[0][1][2][0]==colour && a[0][0][1][0]==colour && a[0][2][1][0]==colour)
        p=1;
        else
        {
            if(a[0][0][1][0]==colour && a[0][2][1][0]==colour)
            execute("FRUruf");
            else if(a[0][1][0][0]==colour && a[0][1][2][0]==colour)
            execute("YFRUruf");
            else
            {
                int found=0;
                for(int i=0;i<4;i++)
                {
                    if(a[0][1][0][0]==colour && a[0][2][1][0]==colour)
                    {
                        found=1;
                        execute("ZBRUruzb");
                        break;
                    }
                    execute("Y");
                }
                if(found==0)
                execute("FRUruf");
            }
        }
        return p;
    }
    
    public int upper_edges()
    {
        int p=0;
        while(a[0][1][0][2]!=a[1][1][0][2])
        execute("U");
        if(a[0][0][1][1]==a[1][0][1][1] && a[0][1][2][4]==a[1][1][2][4] && a[0][2][1][3]==a[1][2][1][3])
        p=1;
        else
        {
            for(int i=0;i<4;i++)
            {
                while(a[0][1][0][2]!=a[1][1][0][2])
                execute("U");
                int count=0;
                for(int j=0;j<4;j++)
                {
                    if(a[0][1][0][2]==a[1][1][0][2])
                    count++;
                    execute("Y");
                }
                if(count>=2)
                break;
                execute("Y");
            }
            
            for(int i=0;i<4;i++)
            {
                if(a[0][2][1][3]==a[1][2][1][3] && a[0][1][2][4]==a[1][1][2][4])
                break;
                execute("Y");
            }
            execute("RUrURUUrU");
            
        }
        return p;
    }
    
    
    public int check_corner()
    {
        int p=1;
        for(int i=0;i<4;i++)
        {
            char colour1=a[0][1][1][0];
            char colour2=a[1][1][0][2];
            char colour3=a[1][2][1][3];
            char c1=a[0][2][0][0];
            char c2=a[0][2][0][2];
            char c3=a[0][2][0][3];
            if((c1!=colour1 && c1!=colour2 && c1!=colour3) || (c2!=colour1 && c2!=colour2 && c2!=colour3) || (c3!=colour1 && c3!=colour2 && c3!=colour3)) 
            p=0;
            execute("Y");
        }
        return p;
    }
    
    public int position_corner()
    {
        int p=0;
        if(check_corner()!=1)
        {
            int found=0;
            for(int i=0;i<4;i++)
            {
            char colour1=a[0][1][1][0];
            char colour2=a[1][1][0][2];
            char colour3=a[1][2][1][3];
            char c1=a[0][2][0][0];
            char c2=a[0][2][0][2];
            char c3=a[0][2][0][3];
            if((c1==colour1 || c1==colour2 || c1==colour3) && (c2==colour1 || c2==colour2 || c2==colour3) && (c3==colour1 || c3==colour2 || c3==colour3)) 
            {
                found=1;
                break;
            }
            execute("Y");
            }
            do
            {
                execute("URulUruL");
            }
            while(found==1 && check_corner()!=1);
        }
        else
        p=1;
        return p;
    }
    
    public int twist()
    {
        int p=0;
        int found=0;
        for(int i=0;i<4;i++)
        {
            if(a[0][2][0][0]!=a[0][1][1][0])
            {
                found=1;
                break;
            }
            execute("U");
        }
        if(found==1)
        {
            while(a[0][2][0][0]!=a[0][1][1][0])
            execute("rdRD");
            
        }
        else
        {
            p=1;
            for(int i=0;i<4;i++)
            {
                if(a[0][1][0][2]==a[1][1][0][2])
                break;
                execute("U");
            }
        }
        return p;
    }
    
    public int reduce(int n,int type)
    {
        int p=1;
        if(type==0)
        {
        for(int i=0;i<(move[n].length()-3);i++)
        {
            char ch=move[n].charAt(i);
            if(ch==move[n].charAt(i+1) && ch==move[n].charAt(i+2) && ch==move[n].charAt(i+3))
            {
                move[n]=move[n].substring(0,i)+move[n].substring(i+4);
                p=0;
                break;
            }
        }
        }
        else if(type==1)
        {
        for(int i=0;i<(move[n].length()-2);i++)
        {
            char ch=move[n].charAt(i);
            if(ch==move[n].charAt(i+1) && ch==move[n].charAt(i+2))
            {
                if(Character.isUpperCase(ch))
                ch=Character.toLowerCase(ch);
                else if(Character.isLowerCase(ch))
                ch=Character.toUpperCase(ch);
                move[n]=move[n].substring(0,i)+ch+move[n].substring(i+3);
                p=0;
                break;
            }
        }
            
        }
        else if(type==2)
        {
        for(int i=0;i<(move[n].length()-1);i++)
        {
            char ch=move[n].charAt(i);
            if(Character.isUpperCase(ch))
                ch=Character.toLowerCase(ch);
                else if(Character.isLowerCase(ch))
                ch=Character.toUpperCase(ch);
            if(ch==move[n].charAt(i+1))
            {
                move[n]=move[n].substring(0,i)+move[n].substring(i+2);
                p=0;
                break;
            }
        }
            
        }
        return p;
    }
    
    public void instruction()
    {
        int n=1;
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<move[i].length();j++)
            {
                char ch=move[i].charAt(j);
                System.out.print(n+": ");
                n++;
                for(int k=0;k<9;k++)
                {
                    if(ch==instruct[k] || ch==(Character.toUpperCase(instruct[k])))
                    {
                        if(k>5)
                        System.out.print("..........................................");
                        System.out.print(ins[k]+" Face ");
                        if(Character.isUpperCase(ch))
                        System.out.println("                  Clockwise");
                        else if(Character.isLowerCase(ch))
                        System.out.println("   Anticlockwise   ");
                        break;
                    }
                }
            }
            if(i==0)
            {
                System.out.println("-------------------------------");
                System.out.println("     First Layer completed");
                System.out.println("-------------------------------");
            }
            else if(i==1)
            {
                System.out.println("-------------------------------");
                System.out.println("     Second Layer completed");
                System.out.println("-------------------------------");
            }
            else
            {
                System.out.println("-------------------------------");
                System.out.println("     Third Layer completed");
                System.out.println("-------------------------------");
            }
        }
    }
    
    public static void main(String []args)throws IOException
    {
        InputStreamReader in=new InputStreamReader(System.in);
        BufferedReader st=new BufferedReader(in);
        Rubiks_cube obj=new Rubiks_cube();
        obj.ini();
        System.out.println("Enter the colours in the six faces");
        System.out.println("W denotes white");
        System.out.println("R denotes red");
        System.out.println("O denotes orange");
        System.out.println("G denotes green");
        System.out.println("B denotes blue");
        System.out.println("Y denotes yellow");
        String s="";
        String name[]={"Front","Upper","Left","Right","Back","Down"};
        for(int j=0;j<6;j++)
        {
            System.out.println(name[j]+" face");
            System.out.println("Enter the colours of the face one by one");
            for(int i=0;i<3;i++)
            {
                String s1=st.readLine();
                s=s+s1;
            }
        }
        s=s.toUpperCase();
        obj.input(s);
        int p=obj.orient();
        
        if(p!=0)
        {
            if(p!=1)
            {
                if(p!=2)
                while(obj.daisy()!=1);
                while(obj.cross()!=1);
            }
            while(obj.first_layer()!=1);
        }
        while(obj.second_layer()!=1);
        while(obj.upper_cross()!=1);
        while(obj.upper_edges()!=1);
        while(obj.position_corner()!=1);
        while(obj.twist()!=1);
        
        for(int i=0;i<3;i++)
        {
            for(int j=0;j<3;j++)
            {
             while(obj.reduce(i,j)!=1);    
            }
        }
        
        System.out.println("                  --------------");
        System.out.println("                     Solution");
        System.out.println("                  --------------");
        System.out.println("----------------------------------------------------------");
        System.out.println("  Follow these instructions to complete the Rubik's Cube");
        System.out.println("----------------------------------------------------------");
        
        obj.instruction();
    }
}
