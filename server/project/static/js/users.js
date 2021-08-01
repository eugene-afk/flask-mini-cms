document.addEventListener('DOMContentLoaded', () => {

    var copyElement = document.querySelector('#copy_creds');
    if(copyElement != null){
    copyElement.addEventListener('click', () =>{
        var text = "Some random text";
        var name = document.querySelector('#sname').value;
        var pwd = document.querySelector('#spassword').value;
        //working only with localhost or https
        navigator.clipboard.writeText(name + '\n' + pwd)
    })
    }

    var copyElement = document.querySelector('#show_pwd');
    if(copyElement != null){
    copyElement.addEventListener('click', () =>{
        var pwd = document.querySelector('#spassword');
        var creds = document.querySelector('#creds');
        pwd.setAttribute('type', 'text');
        creds.style.display = "block";
    })
    }

})