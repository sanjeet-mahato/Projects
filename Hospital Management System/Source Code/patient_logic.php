<?php
$link=mysqli_connect("localhost","root","","hosp");
    if($link==false)
    {
        die("ERROR ".mysqli_connect_error());
    }
    if($_SERVER["REQUEST_METHOD"]=="POST"){
        
        session_start();
        $_SESSION['option']="";
        if(isset($_POST['doctor']))
        {   
             $_SESSION['option']="appo";
            $sql="SELECT * FROM appointment";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_patient.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>APPOINTMENTS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:90px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:18px'>
                <tr style='color:red;font-weight:bold'>
                    <td style='text-align:center'> Date</td>
                   <td style='text-align:center'> Time</td>
                   <td style='text-align:center'> Appointment Id</td>
                    <td style='text-align:center'> Doctor Id</td>
                     <td style='text-align:center'> Name</td>
                    <td style='text-align:center'> Complain</td>
                    <td style='text-align:center'> Status</td>
                    <td style='text-align:center'> Update</td>
                    <td style='text-align:center'> Delete</td>
                </tr>";
            $count=0;
           $date_ch="date$count";
            $appo_ch="appo$count";
            $name_ch="name$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $time_ch="time$count";
            $status_ch="status$count";
            $comp_ch="comp$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            $date="";
            $appo="";
            $pat="";
            $name="new";
             $doc="";
            $time="";
             $comp="";
            $status="";
             
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
            $date=$record['Date'];
             $time=$record['Time'];
            $appo=$record['Appo_Id'];
            $doc=$record['Doc_Id'];
                if($doc=='new')
                    $name='new';
             else
                {
                  $sql2="SELECT * FROM profile";
                $mydata2=mysqli_query($link,$sql2);
                while($record2=mysqli_fetch_array($mydata2))
                {
                if($doc==$record2['User_Id'])
                    $name=$record2['Name'];
                }
                }
            //echo $name;
            $comp=$record['Complain'];
            $status=$record['Status'];
             $pat=$record['Pat_Id'];
            
             if($_SESSION['userid']==$pat)
             echo "<tr><td><input type=text style='text-align:center'  name=$date_ch value='$date' size='10'></td><td><input type=text style='text-align:center'  name=$time_ch value='$time' size='8'></td><td  style='text-align:center' name=$appo_ch value=$appo size='15'>$appo</td><td><input type=text style='text-align:center'  name=$doc_ch value='$doc' size='15'></td><td  style='text-align:center' name=$name_ch value='$name' size='10'>$name</td><td><input type=text style='text-align:center'  name=$comp_ch value='$comp' size='30'></td><td><input type=text style='text-align:center'  name=$status_ch value='$status' size='10'></td><td><input type=submit name=$up_ch value=Update style='background-color:green;font-size:18px;color:white'></td><td><input type=submit name=$del_ch value=Remove style='background-color:red;font-size:18px;color:white'></td></tr>";
             $count=$count+1;
             $date_ch="date$count";
            $appo_ch="appo$count";
            $name_ch="name$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $time_ch="time$count";
            $status_ch="status$count";
            $comp_ch="comp$count";
            $up_ch="up$count";
            $del_ch="del$count";
          }
             echo "</table>";
             echo "<input type=submit value='Add Appointment' name='add_pr' style='background-color:blue;font-size:18px;color:white'/>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['patient']))
        {   
            $_SESSION['option']="pres";
            $sql="SELECT * FROM prescription";
         $mydata=mysqli_query($link,$sql);
            
            echo "<form action=edit_patient.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>PRESCRIPTIONS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:180px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:18px'>
                <tr style='color:red;font-weight:bold'>
                    <td style='text-align:center'> Date</td>
                   <td style='text-align:center'> Prescription Id</td>
                    <td style='text-align:center'> Doctor Id</td>
                    <td style='text-align:center'> Doctor Name</td>
                     <td style='text-align:center'> Medicines</td>
                    <td style='text-align:center'> Advice</td>
                    </tr>";
            $count=0;
            $date_ch="date$count";
            $pres_ch="pres$count";
            $name_ch="name$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $med_ch="med$count";
            $adv_ch="adv$count";
            $up_ch="up$count";
            $del_ch="del$count";
            
            $date="";
            $pres="";
            $pat="";
             $doc="";
            $name="";
             $med="";
            $adv="";
            
         while($record=mysqli_fetch_array($mydata))
         {
             //echo $record['Product']."<br/>";
             $date=$record['Date'];
            $pres=$record['Pres_Id'];
            $doc=$record['Doc_Id'];
            
                  $sql2="SELECT * FROM profile";
                $mydata2=mysqli_query($link,$sql2);
                while($record2=mysqli_fetch_array($mydata2))
                {
                if($doc==$record2['User_Id'])
                    $name=$record2['Name'];
                }
            //echo $name;
            $med=$record['Medicine'];
            $adv=$record['Advice'];
             $pat=$record['Pat_Id'];
            
            if($_SESSION['userid']==$pat)
             echo "<tr><td><input type=text style='text-align:center'  name=$date_ch value='$date' size='10'></td><td  style='text-align:center' name=$pres_ch value=$pres size='15'>$pres</td><td><input type=text style='text-align:center'  name=$doc_ch value='$doc' size='15'><td  style='text-align:center' name=$name_ch value='$name' size='10'>$name</td><td><input type=text style='text-align:center'  name=$med_ch value='$med' size='30'></td><td><input type=text style='text-align:center'  name=$adv_ch value='$adv' size='25'></td></tr>";
             $count=$count+1;
            $date_ch="date$count";
            $pres_ch="pres$count";
            $name_ch="name$count";
            $pat_ch="pat$count";
            $doc_ch="doc$count";
            $med_ch="med$count";
            $adv_ch="adv$count";
            $up_ch="up$count";
            $del_ch="del$count";
           }
             echo "</table>";
                     echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['labo']))
        {   
            $_SESSION['option']="rep";
            $sql="SELECT * FROM report";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_patient.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>REPORTS LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:350px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:18px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> Date</td>
                    <td style='text-align:center'> Report Id</td>
                     <td style='text-align:center'> Doctor Id</td>
                    <td style='text-align:center'> Caption</td>
                    <td style='text-align:center'> Details</td>
                </tr>";
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
             //echo $record['Product']."<br/>";
             $rep=$record['Report_Id'];
             $pat=$record['Pat_Id'];
             $doc=$record['Doc_Id'];
             $capt=$record['Caption'];
             $detail=$record['Details'];
             $lab=$record['Lab_Id'];
             $date=$record['Date'];
             
             if($_SESSION['userid']==$pat)
             echo "<tr><td><input type=text style='text-align:center'  name=$date_ch value='$date' size='12'></td><td  style='text-align:center' name=$rep_ch value=$rep size='15'>$rep</td><td><input type=text style='text-align:center'  name=$doc_ch value=$doc size='15'></td><td><input type=text style='text-align:center'  name=$capt_ch value='$capt' size='10'></td><td><input type=text style='text-align:center'  name=$detail_ch value='$detail' size='20'></td></tr>";
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
             echo "</table>";
                      echo "</div></body></form>"; 
         
        }
        elseif(isset($_POST['account']))
        {   
            $_SESSION['option']='inv';
            $sql="SELECT * FROM invoice";
         $mydata=mysqli_query($link,$sql);
            echo "<form action=edit_account.php method=post>";
           echo "<body style='margin: 0em auto;background-color:#E0FFFF'><div style='height:15px;width:1400px;background-color:teal;'></div><div style='height:100px;width:1400px;background-color:teal;text-align:center;float:left'><h1 style='color:white;font-size:35px'>INVOICE LIST</h1></div><div style='height:40px;width:1400px;float:left;background-color:#E0FFFF'></div><div style='height:700px;width:515px;float:left'></div><div style='position:absolute;left:250px;top:150px;float:center'>";
            echo "<table text-align=center border=1 style='background-color:#F5FFFA;font-size:18px'>
                <tr style='color:red;font-weight:bold'>
                   <td style='text-align:center'> Date</td>
                    <td style='text-align:center'> Invoice Id</td>
                    <td style='text-align:center'> User Id</td>
                    <td style='text-align:center'> User Name</td>
                    <td style='text-align:center'> Accountant Id</td>
                    <td style='text-align:center'> Details</td>
                    <td style='text-align:center'> Amount</td>
                   <td style='text-align:center'> Status</td>
                    
                      </tr>";
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
             //echo $record['Product']."<br/>";
             $date=$record['Date'];
             $inv=$record['Invoice_Id'];
             $pat=$record['Acc_Id'];
             $des=$record['User'];
             $user=$record['User_Id'];
             $detail=$record['Details'];
             $amount=$record['Amount'];
             $status=$record['Status'];
             if($record['Pat_Id']==$_SESSION['userid'])
             echo "<tr><td  style='text-align:center' name=$date_ch value=$date size='12'>$date</td><td  style='text-align:center' name=$inv_ch value=$inv size='15'>$inv</td><td  style='text-align:center' name=$user_ch value=$user size='15'>$user</td><td  style='text-align:center' name=$des_ch value=$des size='15'>$des</td><td  style='text-align:center' name=$pat_ch value=$pat size='15'>$pat</td><td  style='text-align:center' name=$detail_ch value=$detail size='20'>$detail</td><td  style='text-align:center' name=$amount_ch value=$amount size='7'>$amount</td><td  style='text-align:center' name=$status_ch value=$status size='15'>$status</td></tr>";
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