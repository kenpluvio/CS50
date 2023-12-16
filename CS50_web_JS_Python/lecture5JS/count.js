if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter',0);
}

function count() {
    const heading = document.querySelector('h1');
    let counter = localStorage.getItem('counter');
    counter++;
    heading.innerHTML = counter;
    if (counter%10 === 0) {
        alert(`Counter is now ${counter}`)
    }
    localStorage.setItem('counter', counter);
}

document.addEventListener('DOMContentLoaded', ()=>{
    document.querySelector('h1').innerHTML = localStorage.getItem('counter');
    document.querySelector('button').onclick = count;
    
    // setInterval(count, 1000);
})
