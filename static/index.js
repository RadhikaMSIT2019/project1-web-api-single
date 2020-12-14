
document.getElementById('register').addEventListener('click', e =>{
  let mail = document.forms["myForm"]["email"].value;
  let pwrd = document.forms["myForm"]["password"].value;
  let passw = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&.])[A-Za-z\d$@$!%*?&.]{6, 20}/;
  let cmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

  var m = 0;
console.log(cmail.test(mail));
  if (!cmail.test(mail)) {
    // console.log(mail);
    // alert(mail)
    document.getElementById('mail-log').innerHTML = "Enter a valid email";
    m = 1;
  }
  else {
    document.getElementById('mail-log').innerHTML = "";
  }


console.log(passw.test(pwrd));
if (pwrd.match(/[a-z]/g) && pwrd.match(/[A-Z]/g) && pwrd.match(/[0-9]/g) && pwrd.match(/[^a-zA-Z\d]/g) && pwrd.length >= 6)
{
  document.getElementById('password-log').innerHTML = "";
  console.log(false);
}
else
{
  document.getElementById("password-log").innerHTML = "Password should contain atleast one [A-Z],[a-z],[1-0],special characters.";
  m=1;
  console.log(true);
}

  if(m==1)
  {
    // console.log(m);
    // alert(m)
    e.preventDefault();
  }
  else {
    return true;
  }

});

document.getElementById('login').addEventListener('click', e =>{
  let mail = document.forms["myForm"]["email"].value;
  let pwrd = document.forms["myForm"]["password"].value;
  let passw = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&.])[A-Za-z\d$@$!%*?&.]{6, 20}/;
  let cmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

  var m = 0;
console.log(cmail.test(mail));
  if (!cmail.test(mail)) {
    // console.log(mail);
    // alert(mail)
    document.getElementById('mail-log').innerHTML = "Enter a valid email";
    m = 1;
  }
  else {
    document.getElementById('mail-log').innerHTML = "";
  }


console.log(passw.test(pwrd));
if (pwrd.match(/[a-z]/g) && pwrd.match(/[A-Z]/g) && pwrd.match(/[0-9]/g) && pwrd.match(/[^a-zA-Z\d]/g) && pwrd.length >= 6)
{
  document.getElementById('password-log').innerHTML = "";
  console.log(false);
}
else
{
  document.getElementById("password-log").innerHTML = "Password should contain atleast one [A-Z],[a-z],[1-0],special characters.";
  m=1;
  console.log(true);
}

  if(m==1)
  {
    // console.log(m);
    // alert(m)
    e.preventDefault();
  }
  else {
    return true;
  }

});



//paste from here in console of browser





document.getElementById('searchBooks').addEventListener('click', e =>{
  let search = document.getElementById('search').value
  console.log(search);
  let request = new XMLHttpRequest();
  var path = "/api/searchapi/"+search+"/"
  console.log(path);
  request.open("GET", path);
  request.setRequestHeader("Content-Type", "application/json");
  request.send(null);

  request.onload = () => {
    var data = JSON.parse(request.responseText);
    if (request.status === 200) {
      console.log("request recieved");
      console.log(data);

      document.getElementById("dynamic").innerHTML = data["content"];
    } else {
      document.getElementById("dynamic").innerHTML = data["content"];
    }
  };


  return false;
});

function bookdetails(isbn)
{
  console.log(typeof isbn);
  let search = isbn.toString();
  console.log(typeof search);
  let request = new XMLHttpRequest();
  var path = "/api/booksapi/"+search+"/"
  console.log(path);
  request.open("GET", path);
  request.setRequestHeader("Content-Type", "application/json");
  request.send();

  request.onload = () => {
    var data = JSON.parse(request.responseText);
    if (request.status === 200) {
      console.log("request recieved");
      console.log(data);

      document.getElementById("dynamic").innerHTML = data["content"];
    }
  }
}

function review(isbn){
  var ele = document.getElementsByName('rating');
  rating = "" ;

  for(i = 0; i < ele.length; i++) {
      if(ele[i].checked)
      rating = ele[i].value;
  }

  reviews = document.getElementById('Review').value;
  email = document.getElementById('EmailAccess').innerHTML;
  fname = document.getElementById('Fname').innerHTML;


  console.log(typeof isbn);
  let search = isbn.toString();
  console.log(typeof search);
  let request = new XMLHttpRequest();
  var path = "/api/reviewsapi/"+search+"/"+reviews+"/"+rating+"/"+email+"/"+fname+"/";
  console.log(path);
  request.open("GET", path);
  request.setRequestHeader("Content-Type", "application/json");
  request.send();

  request.onload = () => {
    var data = JSON.parse(request.responseText);
    if (request.status === 200) {
      console.log("request recieved");
      console.log(data);

      document.getElementById("dynamic").innerHTML = data["content"];
    }
  }
}
