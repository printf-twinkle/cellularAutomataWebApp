var colorPickers = 1;
var initColor = "#ff0000";
var pickers = document.getElementById("pickers");

const toggleColorPickers = (shouldAdd, toggleIndex) => {
    console.log("toggledd");
  if (shouldAdd) {
    var newPicker = document.createElement("INPUT");
    var id = "picker" + toggleIndex;
    var name = "pick" + toggleIndex;
    newPicker.setAttribute("name",name);
    newPicker.setAttribute("id", id);
    newPicker.setAttribute("value", initColor);
    newPicker.setAttribute("type", "color");
    pickers.appendChild(newPicker);
    pickers.appendChild(document.createElement("BR"));
  } else {
    pickers.removeChild(pickers.lastChild);
    pickers.removeChild(pickers.lastChild);
  }
  console.log("Total child nodes ---" + pickers.childElementCount);
};

const addPicker = () => {
    console.log("entered");
  if (colorPickers === 3) {
    window.alert("Maximum number of pickers reached !!");
  } else {
    console.log("Adding picker");
    toggleColorPickers(true, colorPickers + 1);
    colorPickers++;
  }
  return false;
};
const removePicker = () => {
  if (colorPickers > 1) {
    console.log("Removing picker");
    toggleColorPickers(false, colorPickers);
    colorPickers--;
  } else {
    window.alert("Minimum number of pickers reached !!");
  }
  return false;
};