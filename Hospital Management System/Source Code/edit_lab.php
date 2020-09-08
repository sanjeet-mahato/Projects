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
        $id="RE$id";
        $lab=$_SESSION['userid'];
        
        $gts="INSERT INTO report(Report_Id,Pat_Id,Doc_Id,Lab_Id,Caption,Details,Date) VALUES('$id','new','new','$lab','none','none','dd/mm/yyyy')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Reports \\nEdit Details and Update')</script>";
        
              header("refresh:1 url=lab.php");
        }
        else
        echo "Error".mysqli_error($link);
    }
    elseif(isset($_POST['add_pt']))
    {
        $id=date('mdyhis', time());
        $id="IN$id";
        $user=$_SESSION['userid'];
        $name=$_SESSION['nameses'];
        $gts="INSERT INTO invoice(Date,Invoice_Id,Pat_Id,User,User_Id,Details,Amount,Status,Acc_Id) VALUES('dd/mm/yyyy','$id','new','$name','$user','none','0','Pending','none')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Invoice List \\nEdit Details and Update')</script>";
        
             header("refresh:1 url=lab.php");
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
    elseif($_SESSION['option']=='rep')
        {
            //echo "Not selected";
            $sql="SELECT * FROM report";
            $mydata=mysqli_query($link,$sql);
            $date="";
            $rep="";
            $pat="";
            $doc="";
            $lab="";
            $capt="";
            $detail="";
            
            $up=0;
            $count=0;
            $rep_ch="rep$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $lab_ch="lab$count";
            $capt_ch="capt$count";
            $detail_ch="detail$count";
            $date_ch="date$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
        
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
                 $rep=$record['Report_Id'];
                 
                 $pat=$_POST[$pat_ch];
                 $doc=$_POST[$doc_ch];
                 $capt=$_POST[$capt_ch];
                $detail=$_POST[$detail_ch];
                 $date=$_POST[$date_ch];
                 $up=1;
             }
             elseif(isset($_POST[$del_ch]))
             {    
             $rep=$record['Report_Id'];
                 
             $up=-1;
             }
            
             $count=$count+1;
             $rep_ch="rep$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $lab_ch="lab$count";
            $capt_ch="capt$count";
            $detail_ch="detail$count";
            $date_ch="date$count";
            $up_ch="up$count";
            $del_ch="del$count";
            }   
            $zz="";
        
            if($up==-1)
            {
                $zz="DELETE from report where Report_Id='$rep'";
               // echo $zz;
            }
            elseif($up==1)
            {
                //echo "Entered";
                $zz="UPDATE report SET Pat_Id='$pat',Doc_Id='$doc',Caption='$capt',Details='$detail',Date='$date' WHERE Report_Id='$rep'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=lab.php");
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
                 
                 $pat=$_POST[$pat_ch];
                 $amount=$_POST[$amount_ch];
                 $status=$_POST[$status_ch];
                $detail=$_POST[$detail_ch];
                 $date=$_POST[$date_ch];
                 $up=1;
             }
             elseif(isset($_POST[$del_ch]))
             {    
             $inv=$record['Invoice_Id'];
                    
             $up=-1;
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
        
            if($up==-1)
            {
                $zz="DELETE from invoice where Invoice_Id='$inv'";
               // echo $zz;
            }
            elseif($up==1)
            {
                //echo "Entered";
                $zz="UPDATE invoice SET Date='$date',Pat_Id='$pat',Details='$detail',Amount='$amount',Status='$status' WHERE Invoice_Id='$inv'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=lab.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
}
      mysqli_close($link);
?>