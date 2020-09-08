<?php
$link=mysqli_connect("localhost","root","","hosp");
    if($link==false)
    {
        die("ERROR ".mysqli_connect_error());
    }
    
if($_SERVER["REQUEST_METHOD"]=="POST"){
        
    if(isset($_POST['add_pr']))
    {
        $id=date('mdyhis', time());
        $id="DR$id";
        $gts="INSERT INTO profile(User_Id,Password,User_Type,Department,Name,Sex,Age,Blood_Group,Email_Id,Telephone_No,Address) VALUES('$id','password','Doctor','dep','name','x',0,'x','email','tel','add')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Add/Remove Doctor \\nEdit Details and Update')</script>";
        
              header("refresh:1 url=admin_new.php");
        }
        else
        echo "Error".mysqli_error($link);
    }
    elseif(isset($_POST['add_pt']))
    {
        $id=date('mdyhis', time());
        $id="PT$id";
        $gts="INSERT INTO profile(User_Id,Password,User_Type,Department,Name,Sex,Age,Blood_Group,Email_Id,Telephone_No,Address) VALUES('$id','password','Patient','doctor','name','x',0,'x','email','tel','add')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Add/Remove Patient \\nEdit Details and Update')</script>";
        
             header("refresh:1 url=admin_new.php");
        }
        else
        echo "Error".mysqli_error($link);
    }
    elseif(isset($_POST['add_nr']))
    {
        $id=date('mdyhis', time());
        $id="NR$id";
        $gts="INSERT INTO profile(User_Id,Password,User_Type,Department,Name,Sex,Age,Blood_Group,Email_Id,Telephone_No,Address) VALUES('$id','password','Nurse','dep','name','x',0,'x','email','tel','add')";
        
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Add/Remove Nurse \\nEdit Details and Update')</script>";
        
            header("refresh:1 url=admin_new.php");
        }
        else
        echo "Error".mysqli_error($link);
    }
    elseif(isset($_POST['add_ph']))
    {
        $id=date('mdyhis', time());
        $id="PH$id";
        $gts="INSERT INTO profile(User_Id,Password,User_Type,Department,Name,Sex,Age,Blood_Group,Email_Id,Telephone_No,Address) VALUES('$id','password','Pharmacist','none','name','x',0,'x','email','tel','add')";
        
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Add/Remove Pharmasist \\nEdit Details and Update')</script>";
        
            header("refresh:1 url=admin_new.php");
        }
        else
        echo "Error".mysqli_error($link);
    }
    elseif(isset($_POST['add_lb']))
    {
        $id=date('mdyhis', time());
        $id="LB$id";
        $gts="INSERT INTO profile(User_Id,Password,User_Type,Department,Name,Sex,Age,Blood_Group,Email_Id,Telephone_No,Address) VALUES('$id','password','Laboratorist','none','name','x',0,'x','email','tel','add')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Add/Remove Laboratorist \\nEdit Details and Update')</script>";
        
            header("refresh:1 url=admin_new.php");
        }
        else
        echo "Error".mysqli_error($link);
    }
    elseif(isset($_POST['add_ac']))
    {
        $id=date('mdyhis', time());
        $id="AC$id";
        $gts="INSERT INTO profile(User_Id,Password,User_Type,Department,Name,Sex,Age,Blood_Group,Email_Id,Telephone_No,Address) VALUES('$id','password','Accountant','none','name','x',0,'x','email','tel','add')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Add/Remove Accountant \\nEdit Details and Update')</script>";
        
            header("refresh:1 url=admin_new.php");
        }
        else
        echo "Error".mysqli_error($link);
    }
    else
        {
            //echo "Not selected";
            $sql="SELECT * FROM profile";
            $mydata=mysqli_query($link,$sql);
            $dep="";
            $name="";
            $sex="";
            $age="";
            $blood="";
        
            $em="";
            $tel="";
            $add="";
            $up=0;
            $count=0;
            $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
        
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
                 $user=$record['User_Id'];
                 if($user[1]=='B' || $user[1]=='H' || $user[1]=='C')
                 $dep=$record['Department'];
                 else
                 $dep=$_POST[$dep_ch];
                 
                 $name=$_POST[$name_ch];
                 $sex=$_POST[$sex_ch];
                 $age=$_POST[$age_ch];
                $blood=$_POST[$blood_ch];
                 $em=$_POST[$em_ch];
                 $tel=$_POST[$tel_ch];
                 $add=$_POST[$add_ch];
                 $up=1;
             }
             elseif(isset($_POST[$del_ch]))
             {    
             $user=$record['User_Id'];
             $up=-1;
             }
            
             $count=$count+1;
             $name_ch="name$count";
            $sex_ch="sex$count";
            $age_ch="age$count";
            $blood_ch="blood$count";
            $em_ch="em$count";
            $tel_ch="tel$count";
            $add_ch="add$count";
            $user_ch="user$count";
            $type_ch="type$count";
            $pass_ch="pass$count";
            $dep_ch="dep$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            }   
            $zz="";
        
            if($up==-1)
            {
                $zz="DELETE from profile where User_Id='$user'";
               // echo $zz;
            }
            elseif($up==1)
            {
                //echo "Entered";
                $zz="UPDATE profile SET Department='$dep',Name='$name',Sex='$sex',Age='$age',Blood_Group='$blood',Email_Id='$em',Telephone_No='$tel',Address='$add' WHERE User_Id='$user'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=admin_new.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
}
      mysqli_close($link);
?>