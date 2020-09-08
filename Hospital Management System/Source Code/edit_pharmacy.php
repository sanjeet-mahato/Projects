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
        $id="MD$id";
        $gts="INSERT INTO medicine(Med_Id,Name,Details,Price,Quantity) VALUES('$id','new','none','0','0')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Medicines \\nEdit Details and Update')</script>";
        
              header("refresh:1 url=pharmacy.php");
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
        
             header("refresh:1 url=pharmacy.php");
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
    elseif($_SESSION['option']=='med')
        {
            //echo "Not selected";
            $sql="SELECT * FROM medicine";
            $mydata=mysqli_query($link,$sql);
            $med="";
            $name="";
            $detail="";
            $price="";
            $quant="";
        
            $up=0;
            $count=0;
        
            $med_ch="med$count";
            $name_ch="name$count";
            $detail_ch="detail$count";
            $price_ch="price$count";
            $quant_ch="quant$count";
            $up_ch="up$count";
            $del_ch="del$count";
        
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
                 $med=$record['Med_Id'];
                 $name=$_POST[$name_ch];
                 $detail=$_POST[$detail_ch];
                 $price=$_POST[$price_ch];
                $quant=$_POST[$quant_ch];
                 $up=1;
             }
             elseif(isset($_POST[$del_ch]))
             {    
             $med=$record['Med_Id'];
             $up=-1;
             }
            
             $count=$count+1;
             $med_ch="med$count";
            $name_ch="name$count";
            $detail_ch="detail$count";
            $price_ch="price$count";
            $quant_ch="quant$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            }   
            $zz="";
        
            if($up==-1)
            {
                $zz="DELETE from medicine where Med_Id='$med'";
               // echo $zz;
            }
            elseif($up==1)
            {
                //echo "Entered";
                $zz="UPDATE medicine SET Name='$name',Details='$detail',Price='$price',Quantity='$quant' WHERE Med_Id='$med'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=pharmacy.php");
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
                header("refresh:1 url=pharmacy.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
}
      mysqli_close($link);
?>