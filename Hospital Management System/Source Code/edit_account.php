<?php
$link=mysqli_connect("localhost","root","","hosp");
    if($link==false)
    {
        die("ERROR ".mysqli_connect_error());
    }
    
if($_SERVER["REQUEST_METHOD"]=="POST"){
        session_start();
    if(isset($_POST['add_pr']))
    {
        $id=date('mdyhis', time());
        $id="SA$id";
         $acc=$_SESSION['userid'];
        $gts="INSERT INTO salary(Salary_Id,User_Id,Acc_Id,Date,Amount) VALUES('$id','new','$acc','dd/mm/yyyy','0')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Pay Salary \\nEdit Details and Update')</script>";
        
              header("refresh:1 url=account.php");
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
    elseif($_SESSION['option']=='sal')
        {
            //echo "Not selected";
            $sql="SELECT * FROM salary";
            $mydata=mysqli_query($link,$sql);
            $sal="";
            $user="";
            $acc="";
            $date="";
            $amount="";
        
            $up=0;
            $count=0;
            $sal_ch="sal$count";
            $user_ch="user$count";
            $acc_ch="acc$count";
            $date_ch="date$count";
            $amount_ch="amount$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
        
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
                 $sal=$record['Salary_Id'];
                 
                 $date=$_POST[$date_ch];
                 $user=$_POST[$user_ch];
                 $amount=$_POST[$amount_ch];
                 $up=1;
             }
            
             $count=$count+1;
             $sal_ch="sal$count";
            $user_ch="user$count";
            $acc_ch="acc$count";
            $date_ch="date$count";
            $amount_ch="amount$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            }   
            $zz="";
        
            if($up==1)
            {
                //echo "Entered";
                $zz="UPDATE salary SET Date='$date',User_Id='$user',Amount='$amount' WHERE Salary_Id='$sal'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                header("refresh:1 url=account.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
        elseif($_SESSION['option']=='inv')
        {
            //echo "Not selected";
            $sql="SELECT * FROM invoice";
            $mydata=mysqli_query($link,$sql);
            $date="";
            $inv="";
            $pat="";
            $des="";
            $user="";
            $detail="";
            $status="";
            $lab="";
            
            $up=0;
            $count=0;
            $date_ch="date$count";
            $inv_ch="inv$count";
            $pat_ch="pat$count";
            $des_ch="des$count";
            $user_ch="user$count";
            $detail_ch="detail$count";
            $amount_ch="amount$count";
            $status_ch="status$count";
            $up_ch="up$count";
            $del_ch="del$count";
        
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
                 $inv=$record['Invoice_Id'];
                 $up=1;
             }
             
             $count=$count+1;
             $date_ch="date$count";
            $inv_ch="inv$count";
            $pat_ch="pat$count";
            $des_ch="des$count";
            $user_ch="user$count";
            $detail_ch="detail$count";
            $amount_ch="amount$count";
            $status_ch="status$count";
            $up_ch="up$count";
            $del_ch="del$count";
            }   
            $zz="";
        
            if($up==1)
            {
                //echo "Entered";
                $acceptor=$_SESSION['userid'];
                $zz="UPDATE invoice SET Status='Paid',Acc_Id='$acceptor' WHERE Invoice_Id='$inv'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Accepted Payment')</script>";
                header("refresh:1 url=account.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
}
      mysqli_close($link);
?>