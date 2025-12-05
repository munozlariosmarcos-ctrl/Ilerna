let str = "Peter";
try {
    str.test = 5; 
    alert(str.test); 
} catch (e) {
    console.log("Error:", e);
}