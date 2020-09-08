<?php
    $link=mysqli_connect("localhost","root","","hosp");
    if($link==false)
    {
        die("ERROR ".mysqli_connect_error());
    }
    if($_SERVER["REQUEST_METHOD"]=="POST"){
        
        if(isset($_POST['logged']))
        {
          session_start();
            //echo "Trying to login";
            $sel=$_POST['user_type'];
            $given_id=$_POST['user_id'];
            $given_pass=$_POST['pass'];
            
            if($sel==1)
            {
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $p=0;
           while($record=mysqli_fetch_array($mydata))
         {
             $user_id=$record['User_Id'];
                $pass=$record['Password'];
               
              if($user_id==$given_id && $pass==$given_pass)
              {
                  $_SESSION['userid']=$user_id;
                  $_SESSION['nameses']=$record['Name'];
                  $_SESSION['selected']=$sel;
                  
                  header("refresh:1 url=admin_new.php ");
                  $p=1;
              }
               
         } 
                
                if($p==0)
                {
                    echo "<script type='text/Javascript'>alert('Wrong ID or Password ')</script>";
                    header("refresh:1; url=login_new.html");
                }
            }
            elseif($sel==2)
            {
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $p=0;
           while($record=mysqli_fetch_array($mydata))
         {
             $user_id=$record['User_Id'];
                $pass=$record['Password'];
               
              if($user_id==$given_id && $pass==$given_pass)
              {
                  $_SESSION['userid']=$user_id;
                  $_SESSION['nameses']=$record['Name'];
                  $_SESSION['selected']=$sel;
                  
                  header("refresh:1 url=doctor.php ");
                  $p=1;
              }
               
         } 
                
                if($p==0)
                {
                    echo "<script type='text/Javascript'>alert('Wrong ID or Password ')</script>";
                    header("refresh:1; url=login_new.html");
                }
            }
            elseif($sel==3)
            {
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $p=0;
           while($record=mysqli_fetch_array($mydata))
         {
             $user_id=$record['User_Id'];
                $pass=$record['Password'];
               
              if($user_id==$given_id && $pass==$given_pass)
              {
                   // echo "Enteresd";
                  $_SESSION['userid']=$user_id;
                  $_SESSION['nameses']=$record['Name'];
                  $_SESSION['selected']=$sel;
                  
                  header("refresh:1 url=patient.php ");
                  $p=1;
              }
               
         } 
                
                if($p==0)
                {
                    echo "<script type='text/Javascript'>alert('Wrong ID or Password ')</script>";
                    header("refresh:1; url=login_new.html");
                }
            }
            elseif($sel==4)
            {
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $p=0;
           while($record=mysqli_fetch_array($mydata))
         {
             $user_id=$record['User_Id'];
                $pass=$record['Password'];
               
              if($user_id==$given_id && $pass==$given_pass)
              {
                  $_SESSION['userid']=$user_id;
                  $_SESSION['nameses']=$record['Name'];
                  $_SESSION['selected']=$sel;
                  
                  header("refresh:1 url=nurse.php ");
                  $p=1;
              }
               
         } 
                
                if($p==0)
                {
                    echo "<script type='text/Javascript'>alert('Wrong ID or Password ')</script>";
                    header("refresh:1; url=login_new.html");
                }
            }
            elseif($sel==5)
            {
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $p=0;
           while($record=mysqli_fetch_array($mydata))
         {
             $user_id=$record['User_Id'];
                $pass=$record['Password'];
               
              if($user_id==$given_id && $pass==$given_pass)
              {
                  $_SESSION['userid']=$user_id;
                  $_SESSION['nameses']=$record['Name'];
                  $_SESSION['selected']=$sel;
                  
                  header("refresh:1 url=pharmacy.php ");
                  $p=1;
              }
               
         } 
                
                if($p==0)
                {
                    echo "<script type='text/Javascript'>alert('Wrong ID or Password ')</script>";
                    header("refresh:1; url=login_new.html");
                }
            }
            elseif($sel==6)
            {
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $p=0;
           while($record=mysqli_fetch_array($mydata))
         {
             $user_id=$record['User_Id'];
                $pass=$record['Password'];
               
              if($user_id==$given_id && $pass==$given_pass)
              {
                  $_SESSION['userid']=$user_id;
                  $_SESSION['nameses']=$record['Name'];
                  $_SESSION['selected']=$sel;
                  
                  header("refresh:1 url=lab.php ");
                  $p=1;
              }
               
         } 
                
                if($p==0)
                {
                    echo "<script type='text/Javascript'>alert('Wrong ID or Password ')</script>";
                    header("refresh:1; url=login_new.html");
                }
            }
            elseif($sel==7)
            {
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $p=0;
           while($record=mysqli_fetch_array($mydata))
         {
             $user_id=$record['User_Id'];
                $pass=$record['Password'];
               
              if($user_id==$given_id && $pass==$given_pass)
              {
                  $_SESSION['userid']=$user_id;
                  $_SESSION['nameses']=$record['Name'];
                  $_SESSION['selected']=$sel;
                  
                  header("refresh:1 url=account.php ");
                  $p=1;
              }
               
         } 
                
                if($p==0)
                {
                    echo "<script type='text/Javascript'>alert('Wrong ID or Password ')</script>";
                    header("refresh:1; url=login_new.html");
                }
            }
            else
            {
                echo "<script type='text/Javascript'>alert('Please choose a Category ')</script>";
                    header("refresh:1; url=login_new.html");
            }
            
            
        }
    }

?>