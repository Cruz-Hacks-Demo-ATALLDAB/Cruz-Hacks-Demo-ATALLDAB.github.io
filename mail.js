const firebaseConfig = {
    apiKey: "AIzaSyCymdaMs4v-T6I17vXtqOEWkoa7gZGBcH0",
    authDomain: "cruzhacks-c022a.firebaseapp.com",
    databaseURL: "https://cruzhacks-c022a-default-rtdb.firebaseio.com",
    projectId: "cruzhacks-c022a",
    storageBucket: "cruzhacks-c022a.appspot.com",
    messagingSenderId: "548963977111",
    appId: "1:548963977111:web:c40314b14896b7708826d2",
    measurementId: "G-4RTYT6C79B"
};

firebase.initializeApp(firebaseConfig);
var contactFormDB = firebase.database().ref('contactForm');

document.getElementById('contactForm').addEventListener('submit', submitForm);

function submitForm(e){
    e.preventDefault();

    var currentPeopleCount = getElementVal('current-people-count');

    console.log(currentPeopleCount);

    // Save the current people count to the database
    contactFormDB.push().set({
        currentPeopleCount: currentPeopleCount,
        timestamp: firebase.database.ServerValue.TIMESTAMP
    });

    // You can add additional logic here if needed
}

const getElementVal = (id) =>{
    return document.getElementById(id).value;
};
