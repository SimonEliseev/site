window.addEventListener('DOMContentLoaded', () => {
    shuffle(document.querySelector('#yandex'));
    shuffle(document.querySelector('#tinkoff'));
    // let urbamatica = document.querySelector('#ulvac');
    // let wellyes = document.querySelector('#ulvac');

    function shuffle(companyVac) {
        console.log(companyVac)
        for (let i = companyVac.children.length; i >= 0; i--) {
            companyVac.appendChild(companyVac.children[Math.random() * i | 0]);
            console.log(companyVac.children.length)
        }
    }

});