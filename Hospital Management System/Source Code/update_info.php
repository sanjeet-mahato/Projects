<?php
$link=mysqli_connect("localhost","root","","hosp");
    if($link==false)
    {
        die("ERROR ".mysqli_connect_error());
    }
    
if($_SERVER["REQUEST_METHOD"]=="POST"){
     
    session_start();
    $user=$_SESSION['userid'];
    if(isset($_POST['up_info']))
    {
        $pass=$_POST['passw'];
         $sex=$_POST['sex'];
        $age=$_POST['age'];
        $blood=$_POST['bg'];       
        $em=$_POST['eml'];
        $tel=$_POST['tele'];
        $add=$_POST['addr'];
        
        

        $zz="UPDATE profile SET Password='$pass',Sex='$sex',Age='$age',Blood_Group='$blood',Email_Id='$em',Telephone_No='$tel',Address='$add' WHERE User_Id='$user'";
        
        if(mysqli_query($link,$zz))
        {
            echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
            if($user[0]=='A' && $user[1]=='D')
            header("refresh:1 url=admin_new.php");
            elseif($user[0]=='D' && $user[1]=='R')
            header("refresh:1 url=doctor.php");
            elseif($user[0]=='P' && $user[1]=='T')
            header("refresh:1 url=patient.php");
            elseif($user[0]=='N' && $user[1]=='R')
            header("refresh:1 url=nurse.php");
            elseif($user[0]=='P' && $user[1]=='H')
            header("refresh:1 url=pharmacy.php");
            elseif($user[0]=='L' && $user[1]=='B')
            header("refresh:1 url=lab.php");
            elseif($user[0]=='A' && $user[1]=='C')
            header("refresh:1 url=account.php");
            
        }
        else
        echo "Error".mysqli_error($link);
        
        
    }
    
}
      mysqli_close($link);
?>