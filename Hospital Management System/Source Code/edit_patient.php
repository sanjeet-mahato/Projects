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
        $id="AP$id";
        $pat=$_SESSION['userid'];
        $gts="INSERT INTO appointment(Appo_Id,Pat_Id,Doc_Id,Date,Time,Complain,Status) VALUES('$id','$pat','new','dd/mm/yyyy','00:00','none','pending')";
       if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Add Appointment \\nEdit Details and Update')</script>";
        
              header("refresh:1 url=patient.php");
        }
        else
        echo "Error".mysqli_error($link);
    }
    elseif(isset($_POST['add_pt']))
    {
        $id=date('mdyhis', time());
        $id="PR$id";
        $doc=$_SESSION['userid'];
        $gts="INSERT INTO prescription(Pres_Id,Pat_Id,Doc_Id,Medicine,Advice,Date) VALUES('$id','new','$doc','none','none','dd/mm/yyyy')";
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
    else if($_SESSION['option']=='appo')
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
            $doc=$_POST[$doc_ch];
             $comp=$_POST[$comp_ch];
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
                $zz="UPDATE appointment SET Doc_Id='$doc',Date='$date',Time='$time',Complain='$comp',Status='$status' WHERE Appo_Id='$appo'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=patient.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
}
      mysqli_close($link);
?>