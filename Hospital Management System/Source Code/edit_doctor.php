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
        $id="PR$id";
        $doc=$_SESSION['userid'];
        $gts="INSERT INTO prescription(Pres_Id,Pat_Id,Doc_Id,Nurse_Id,Medicine,Advice,Date) VALUES('$id','new','$doc','none','none','none','dd/mm/yyyy')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Prescriptions \\nEdit Details and Update')</script>";
        
             header("refresh:1 url=doctor.php");
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
    elseif($_SESSION['option']=='pres')
        {
        //echo "Entered";
            //echo "Not selected";
           $sql="SELECT * FROM prescription";
            $mydata=mysqli_query($link,$sql);
            $count=0;
            $date_ch="date$count";
            $pres_ch="pres$count";
            $name_ch="name$count";
            $nurname_ch="nurname$count";
            $pat_ch="pat$count";
            $nur_ch="nur$count";
            $doc_ch="doc$count";
            $med_ch="med$count";
            $adv_ch="adv$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            $date="";
            $pres="";
            $pat="";
            $name="";
            $nur="";
            $nurname="";
             $doc="";
             $med="";
            $adv="";
            
        
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
            $date=$_POST[$date_ch];
            $pres=$record['Pres_Id'];
            $pat=$_POST[$pat_ch];
            $nur=$_POST[$nur_ch];     
             $med=$_POST[$med_ch];
            $adv=$_POST[$adv_ch];
            
                 $up=1;
             }
             elseif(isset($_POST[$del_ch]))
             {    
             $pres=$record['Pres_Id'];
             $up=-1;
             }
            
             $count=$count+1;
            $date_ch="date$count";
            $pres_ch="pres$count";
            $name_ch="name$count";
            $nurname_ch="nurname$count";
            $pat_ch="pat$count";
            $nur_ch="nur$count";
            $doc_ch="doc$count";
            $med_ch="med$count";
            $adv_ch="adv$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            
            }   
            $zz="";
        
            if($up==-1)
            {
                $zz="DELETE from prescription where Pres_Id='$pres'";
               // echo $zz;
            }
            elseif($up==1)
            {
                //echo "Entered";
                $zz="UPDATE prescription SET Pat_Id='$pat',Nurse_Id='$nur',Medicine='$med',Advice='$adv',Date='$date' WHERE Pres_Id='$pres'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=doctor.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
    elseif($_SESSION['option']=='appo')
        {
        //echo "Entered";
            //echo "Not selected";
           $sql="SELECT * FROM appointment";
            $mydata=mysqli_query($link,$sql);
            $count=0;
            $date_ch="date$count";
            $time_ch="time$count";
            $appo_ch="appo$count";
            $name_ch="name$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $comp_ch="comp$count";
            $status_ch="status$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            $date="";
            $time="";
            $appo="";
            $pat="";
            $name="";
             $doc="";
             $comp="";
            $status="";
            
        
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
            $date=$_POST[$date_ch];
            $time=$_POST[$time_ch]; 
            $appo=$record['Appo_Id'];
            $status=$_POST[$status_ch];
                 $up=1;
             }
             elseif(isset($_POST[$del_ch]))
             {    
             $appo=$record['Appo_Id'];
             $up=-1;
             }
            
             $count=$count+1;
            $date_ch="date$count";
            $time_ch="time$count";
            $appo_ch="appo$count";
            $name_ch="name$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $comp_ch="comp$count";
            $status_ch="status$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            
            }   
            $zz="";
        
            if($up==-1)
            {
                $zz="DELETE from appointment where Appo_Id='$appo'";
               // echo $zz;
            }
            elseif($up==1)
            {
                //echo "Entered";
                $zz="UPDATE appointment SET Date='$date',Time='$time',Status='$status' WHERE Appo_Id='$appo'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=doctor.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
}
      mysqli_close($link);
?>