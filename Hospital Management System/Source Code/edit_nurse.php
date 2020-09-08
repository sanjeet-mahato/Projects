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
        $id="MT$id";
        $nur=$_SESSION['userid'];
        $gts="INSERT INTO monitor(Mon_Id,Pat_Id,Nurse_Id,Doc_Id,Date,BP,Temp,Other) VALUES('$id','new','$nur','new','dd/mm/yyyy','none','0 F','none')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Monitor Patient \\nEdit Details and Update')</script>";
        
             header("refresh:1 url=nurse.php");
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
        $id="BD$id";
        $nur=$_SESSION['userid'];
        $gts="INSERT INTO bed(Bed_Id,Nurse_Id,Pat_Id) VALUES('$id','$nur','new')";
        if(mysqli_query($link,$gts))
        {
            echo "<script type='text/Javascript'>alert('New Record Sucessfully Inserted\\nOpen Bed Allotment \\nEdit Details and Update')</script>";
        
            header("refresh:1 url=nurse.php");
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
    elseif($_SESSION['option']=='bed')
        {
        //echo "Entered";
            //echo "Not selected";
           $sql="SELECT * FROM bed";
            $mydata=mysqli_query($link,$sql);
            $count=0;
            $bed_ch="bed$count";
            $pat_ch="pat$count";
            $nur_ch="nur$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            $bed="";
            $pat="";
            $nur="";
        
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
                $pat=$_POST[$pat_ch];
                 $bed=$record['Bed_Id'];
                 $up=1;
             }
             elseif(isset($_POST[$del_ch]))
             {    
                 $bed=$record['Bed_Id'];
             $up=-1;
             }
            
             $count=$count+1;
            $bed_ch="bed$count";
            $pat_ch="pat$count";
            $nur_ch="nur$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            
            }   
            $zz="";
        
            if($up==-1)
            {
                $zz="DELETE from bed where Bed_Id='$bed'";
               // echo $zz;
            }
            elseif($up==1)
            {
                //echo "Entered";
                $zz="UPDATE bed SET Pat_Id='$pat' WHERE Bed_Id='$bed'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=nurse.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
        elseif($_SESSION['option']=='mon')
        {
        //echo "Entered";
            //echo "Not selected";
           $sql="SELECT * FROM monitor";
            $mydata=mysqli_query($link,$sql);
            $count=0;
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $date_ch="date$count";
            $bp_ch="bp$count";
            $temp_ch="temp$count";
            $other_ch="other$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            
            $pat="";
            $doc="";
            $date="";
            $bp="";
            $temp="";
            $other="";
            $mon="";
            
        
            while($record=mysqli_fetch_array($mydata))
            {
             //echo $try;
             if(isset($_POST[$up_ch]))
             {    
                $pat=$_POST[$pat_ch];
                $doc=$_POST[$doc_ch];
                $date=$_POST[$date_ch];
                $bp=$_POST[$bp_ch];
                $temp=$_POST[$temp_ch];
                $other=$_POST[$other_ch];
                 $mon=$record['Mon_Id'];
                 $up=1;
             }
             elseif(isset($_POST[$del_ch]))
             {    
                 $mon=$record['Mon_Id'];
             $up=-1;
             }
            
             $count=$count+1;
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $date_ch="date$count";
            $bp_ch="bp$count";
            $temp_ch="temp$count";
            $other_ch="other$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            
            }   
            $zz="";
        
            if($up==-1)
            {
                $zz="DELETE from monitor where Mon_Id='$mon'";
               // echo $zz;
            }
            elseif($up==1)
            {
                //echo "Entered";
                $zz="UPDATE monitor SET Pat_Id='$pat',Doc_Id='$doc',Date='$date',BP='$bp',Temp='$temp',Other='$other' WHERE Mon_Id='$mon'";
            }
            
            
            if(mysqli_query($link,$zz))
            {
                if($up==1)
                echo "<script type='text/Javascript'>alert('Successfully Updated Record')</script>";
                elseif($up==-1)
                echo "<script type='text/Javascript'>alert('Successfully Deleted Record')</script>";
                header("refresh:1 url=nurse.php");
            }
            else
            echo "Error".mysqli_error($link);
            
        }
}
      mysqli_close($link);
?>