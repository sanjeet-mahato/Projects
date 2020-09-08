<?php
$link=mysqli_connect("localhost","root","","hosp");
    if($link==false)
    {
        die("ERROR ".mysqli_connect_error());
    }
    if($_SERVER["REQUEST_METHOD"]=="POST"){
        
        session_start();
        if(isset($_POST['doctor']))
        {   
            $_SESSION['option']="pres";
            $sql="SELECT * FROM prescription";
         $mydata=mysqli_query($link,$sql);
            
            echo "<form action=edit_nurse.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>PRESCRIPTIONS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:100px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:16px'>
                <tr style='color:red;font-weight:bold'>
                    <td style='text-align:center'> Date</td>
                   <td style='text-align:center'> Prescription Id</td>
                    <td style='text-align:center'> Doctor Id</td>
                    <td style='text-align:center'> Doctor Name</td>
                    <td style='text-align:center'> Patient Id</td>
                    <td style='text-align:center'> Patient Name</td>
                     <td style='text-align:center'> Medicines</td>
                    <td style='text-align:center'> Advice</td>
                    </tr>";
            $count=0;
            $date_ch="date$count";
            $pres_ch="pres$count";
            $name_ch="name$count";
            $nur_ch="nur$count";
            $patname_ch="patname$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $med_ch="med$count";
            $adv_ch="adv$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            $date="";
            $pres="";
            $pat="";
            $patname="";
            $nur="";
             $doc="";
            $name="";
             $med="";
            $adv="";
            $temp=0;
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $date=$record['Date'];
            $pres=$record['Pres_Id'];
            $doc=$record['Doc_Id'];
             $pat=$record['Pat_Id'];
            
                  $sql2="SELECT * FROM profile";
                $mydata2=mysqli_query($link,$sql2);
                while($record2=mysqli_fetch_array($mydata2))
                {
                if($doc==$record2['User_Id'])
                    $name=$record2['Name'];
                }
             if($pat=='new')
             {
                 $patname='new';
                 $temp=0;
             }
             else
             {
                 $temp=1;
                  $sql3="SELECT * FROM profile";
                $mydata3=mysqli_query($link,$sql3);
                while($record3=mysqli_fetch_array($mydata3))
                {
                if($pat==$record3['User_Id'])
                    $patname=$record3['Name'];
                }
             }
             
            //echo $name;
            $med=$record['Medicine'];
            $adv=$record['Advice'];
             $nur=$record['Nurse_Id'];
            
            if($_SESSION['userid']==$nur && $temp==1)
             echo "<tr><td><input type=text style='text-align:center'  name=$date_ch value='$date' size='10'></td><td  style='text-align:center' name=$pres_ch value=$pres size='15'>$pres</td><td><input type=text style='text-align:center'  name=$doc_ch value='$doc' size='15'><td  style='text-align:center' name=$name_ch value='$name' size='10'>$name</td><td><input type=text style='text-align:center'  name=$pat_ch value='$pat' size='15'><td  style='text-align:center' name=$patname_ch value='$patname' size='10'>$patname</td><td><input type=text style='text-align:center'  name=$med_ch value='$med' size='30'></td><td><input type=text style='text-align:center'  name=$adv_ch value='$adv' size='25'></td></tr>";
             $count=$count+1;
            $date_ch="date$count";
            $pres_ch="pres$count";
            $name_ch="name$count";
             $patname_ch="patname$count";
            $pat_ch="pat$count";
            $nur_ch="nur$count";
            $doc_ch="doc$count";
            $med_ch="med$count";
            $adv_ch="adv$count";
            $up_ch="up$count";
            $del_ch="del$count";
           }
             echo "</table>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['patient']))
        {   
             $_SESSION['option']="mon";
            $sql="SELECT * FROM monitor";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_nurse.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>PATIENT CONDITION LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:60px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:14px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> Date</td>
                    <td style='text-align:center'> Monitor Id</td>
                    <td style='text-align:center'> Doctor Id</td>
                    <td style='text-align:center'> Doctor Name</td>
                    <td style='text-align:center'> Patient Id</td>
                     <td style='text-align:center'> Patient Name</td>
                   <td style='text-align:center'> Blood Pressure</td>
                    <td style='text-align:center'> Temperature</td>
                    <td style='text-align:center'> Other Symptoms</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
            $date_ch="date$count";
            $mon_ch="mon$count";
            $doc_ch="doc$count";
            $docname_ch="docname$count";
            $pat_ch="pat$count";
            $patname_ch="patname$count";
            $bp_ch="bp$count";
            $temp_ch="temp$count";
            $other_ch="other$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            $date="";
            $mon="";
            $doc="new";
            $nur="";
            $docname="";
            $pat="new";
            $patname="";
            $bp="";
            $temp="";
            $other="";
            
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
            
             $date=$record['Date'];
            $mon=$record['Mon_Id'];
            $doc=$record['Doc_Id'];
            $pat=$record['Pat_Id'];
             $nur=$record['Nurse_Id'];
            $bp=$record['BP'];
            $temp=$record['Temp'];
            $other=$record['Other'];
             
             if($pat=='new')
            $patname='new';
             else
            {
                  $sql2="SELECT * FROM profile";
                $mydata2=mysqli_query($link,$sql2);
                while($record2=mysqli_fetch_array($mydata2))
                {
                if($pat==$record2['User_Id'])
                    $patname=$record2['Name'];
                }
             }//echo $name;
             
             if($doc=='new')
            $docname='new';
             else
            {
                  $sql3="SELECT * FROM profile";
                $mydata3=mysqli_query($link,$sql3);
                while($record3=mysqli_fetch_array($mydata3))
                {
                if($doc==$record3['User_Id'])
                    $docname=$record3['Name'];
                }
             }//echo $name;
             
             if($_SESSION['userid']==$nur)
             echo "<tr><td><input type=text style='text-align:center'  name=$date_ch value='$date' size='12'></td><td  style='text-align:center' name=$mon_ch value=$mon size='15'>$mon</td><td><input type=text style='text-align:center'  name=$doc_ch value='$doc' size='15'></td><td  style='text-align:center' name=$docname_ch value=$docname size='15'>$docname</td><td><input type=text style='text-align:center'  name=$pat_ch value='$pat' size='15'></td><td  style='text-align:center' name=$patname_ch value=$patname size='15'>$patname</td><td><input type=text style='text-align:center'  name=$bp_ch value=$bp size='10'></td><td><input type=text style='text-align:center'  name=$temp_ch value=$temp size='6'></td><td><input type=text style='text-align:center'  name=$other_ch value=$other size='15'></td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $date_ch="date$count";
            $mon_ch="mon$count";
            $doc_ch="doc$count";
            $docname_ch="docname$count";
            $pat_ch="pat$count";
            $patname_ch="patname$count";
            $bp_ch="bp$count";
            $temp_ch="temp$count";
            $other_ch="other$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             echo "<input type=submit value='Add Patient' name='add_pt' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['labo']))
        {   
            $_SESSION['option']="bed";
            $sql="SELECT * FROM bed";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_nurse.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>ALLOTED BED LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:400px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:18px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> Bed Id</td>
                    <td style='text-align:center'> Patient Id</td>
                     <td style='text-align:center'> Patient Name</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
            $bed_ch="bed$count";
            $name_ch="name$count";
            $pat_ch="pat$count";
            $nur_ch="nur$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            $bed="";
            $name="new";
            $pat="";
            $nur="";
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $bed=$record['Bed_Id'];
            $pat=$record['Pat_Id'];
             $nur=$record['Nurse_Id'];
             
            if($pat=='new')
                    $name='new';
             else
                {
                  $sql2="SELECT * FROM profile";
                $mydata2=mysqli_query($link,$sql2);
                while($record2=mysqli_fetch_array($mydata2))
                {
                if($pat==$record2['User_Id'])
                    $name=$record2['Name'];
                }
                }
             
             if($_SESSION['userid']==$nur)
             echo "<tr><td  style='text-align:center' name=$bed_ch value=$bed size='10'>$bed</td><td><input type=text style='text-align:center'  name=$pat_ch value='$pat' size='15'></td><td  style='text-align:center' name=$name_ch value=$name size='10'>$name</td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $bed_ch="bed$count";
            $name_ch="name$count";
            $pat_ch="pat$count";
            $nur_ch="nur$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             echo "<input type=submit value='Add Bed' name='add_lb' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['account']))
        {   
            $_SESSION['option']='sal';
            $sql="SELECT * FROM salary";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_nurse.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>SALARY HISTORY</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:450px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:18px'>
                <tr style='color:red;font-weight:bold'>
                <td style='text-align:center'> Date</td>
                   <td style='text-align:center'> Salary Id</td>
                     <td style='text-align:center'> Accountant Id</td>
                     <td style='text-align:center'> Amount</td>
                </tr>";
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
             //echo $record['Product']."<br/>";
             $date=$record['Date'];
             $user=$record['User_Id'];
             $acc=$record['Acc_Id'];
             $sal=$record['Salary_Id'];
             $amount=$record['Amount'];
             if($_SESSION['userid']==$user)
             echo "<tr><td><input type=text style='text-align:center'  name=$date_ch value='$date' size='12'></td><td  style='text-align:center' name=$sal_ch value=$sal size='15'>$sal</td><td><input type=text style='text-align:center'  name=$acc_ch value='$acc' size='15'></td><td><input type=text style='text-align:center'  name=$amount_ch value=$amount size='7'></td></tr>";
             $count=$count+1;
             $sal_ch="sal$count";
            $user_ch="user$count";
            $acc_ch="acc$count";
            $date_ch="date$count";
            $amount_ch="amount$count";
            $up_ch="up$count";
            $del_ch="del$count";
         }
             echo "</table>";
             
                     echo "</div></body></form>"; 
         
         
        }
        elseif(isset($_POST['log_out']))
        {
            echo "<script type='text/Javascript'>
            alert('Successfully Logged Out')</script>";
            $_SESSION['selected']=0;
            header("refresh:1 url=login_new.html");
        }
        elseif(isset($_POST['info']))
        {
            //echo "Personal information Selected";
         
            $sql="SELECT * FROM profile";
         $mydata=mysqli_query($link,$sql);
                $pass="";
                $sex="";
                $age="";
                $blood="";
                 $em="";
                 $tel="";
                 $address="";
                
         while($record=mysqli_fetch_array($mydata))
         {
             if($_SESSION['userid']==$record['User_Id'])
             {
                 $pass=$record['Password'];
                 $sex=$record['Sex'];
                $age=$record['Age'];
                $blood=$record['Blood_Group'];
                 $em=$record['Email_Id'];
                 $tel=$record['Telephone_No'];
                 $address=$record['Address'];
             }
             
         }
            
            echo "<form action=update_info.php method=post>";
            echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>PERSONAL INFORMATION</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='float:center'>";
            echo "<table border=1 style='background-color:#F5FFFA;font-size:24px'>
                  <tr> 
                    <td style='color:red;font-weight:bold'> User Id</td><td>".$_SESSION['userid']."</td></tr><tr><td style='color:red;font-weight:bold'> Name</td><td>".$_SESSION['nameses']."</td></tr><tr><td style='color:red;font-weight:bold'> Password</td><td><input type=password name='passw' value=$pass size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Sex </td><td><input type=text name='sex' value=$sex size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Age </td><td><input type=text name='age' value=$age size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Blood Group </td><td><input type=text name='bg' value=$blood size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Email Id</td><td><input type=text name='eml' value=$em size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Telephone No</td><td><input type=text name='tele' value=$tel size='20'></td></tr><tr><td style='color:red;font-weight:bold'> Address</td><td><input type=text name='addr' value='$address' size='20'></td></tr>
                    </table>";
             echo "<input type=submit value='Update' name='up_info' style='background-color:green;font-size:20px;color:white'/></div></body></form>";
        }
    }
?>