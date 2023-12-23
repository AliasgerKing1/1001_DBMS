const routes = require("express").Router();
const sha1 = require("sha1")
const Dbms_table = require("../models/Dbms_table");
const jwt = require("jsonwebtoken")

routes.post("/",  async(req,res) => {
    body = req.body

    let is_exist_table = await Dbms_table.find({table_name : body.table_name})
    if(is_exist_table.length == 0 ) {
      body?.property_lst?.map((property) => (
        property.count = parseInt(property.count)
    ))
    let result = await Dbms_table.create(body);
    res.send({status : 200, success : true, data : result})
    }
    else 
        res.send({ status: 400, success: false, data: body?.table_name });
    
})
routes.post("/data", async (req, res) => {
  const body = req.body;
  try {
      if (body?.what_to_select.trim() === "*") {
          // If what_to_select is "*", fetch all data
          let result = await Dbms_table.find({table_name : body?.table_name});
          if(result.length > 0) {
        res.send({ status: 200, success: true, data: result[0] });
      }
        else 
        res.send({ status: 400, success: false, data: body?.table_name });
      }
  } catch (error) {
      res.status(500).send({ status: 500, success: false, error: "Internal Server Error" });
  }
});
routes.post("/data/lst", async (req, res) => {
  const body = req.body;

  try {
    if (Array.isArray(body?.what_to_select) && body?.what_to_select.length > 0) {
      // If what_to_select is an array, fetch data for each property one by one
      const results = await Promise.all(body.what_to_select.map(async (property) => {
        if (property.trim() === "*") {
          // If property is "*", fetch all data
          const result = await Dbms_table.find({ table_name: body?.table_name });
          return { property, data: result[0] };
        } else {
          const document = await Dbms_table.findOne({ "property_lst.name": property });

          if (document) {
            const index = document.property_lst.findIndex((prop) => prop.name === property);

            if (index !== -1 && document.actual_data) {
              // Extract the selected property from all objects in actual_data
              const selectedData = document.actual_data.map((obj) => obj[`prop${index}`]);
              return { property, data: { selectedData, matchedPropertyName: property } };
            } else {
              return { property, data: {} };
            }
          } else {
            return { property, data: {} };
          }
        }
      }));

      res.send({ status: 200, success: true, data: results });
    } else {
      res.send({ status: 200, success: true, data: {} });
    }
  } catch (error) {
    res.status(500).send({ status: 500, success: false, error: "Internal Server Error" });
  }
});

routes.post("/delete/table", async (req, res) => {
let result = await Dbms_table.find({table_name : req?.body?.which_table_to_delete})

// await Dbms_table.deleteMany({table_name : req?.body?.which_table_to_delete})
res.send({ status: 400, success: true});
// res.send({ status: 200, success: true, data: req?.body?.which_table_to_delete });
});
routes.post("/delete/row", async (req, res) => {
let find_table_to_delete_row =  await Dbms_table.find({table_name : req?.body?.from_which_table}) 
let whichRowToDelete = req.body.which_row_to_delete;
let new_row_with_filtered;
// console.log(whichRowToDelete)
// Ensure whichRowToDelete is an array and not empty
if (Array.isArray(whichRowToDelete) && whichRowToDelete.length > 0) {
  // Convert items to integers
  let rowIndicesToDelete = whichRowToDelete.map(item => parseInt(item, 10));
  

  console.log("Row Indices to Delete:", rowIndicesToDelete);

  // Assuming find_table_to_delete_row[0] exists
  let actualData = find_table_to_delete_row[0]?.actual_data;

  // Ensure actualData is not undefined or null
  if (actualData) {
    new_row_with_filtered = actualData.filter((data, index) => !rowIndicesToDelete.includes(index));

    // console.log("Filtered Rows:", new_row_with_filtered);
  } else {
    console.log("actual_data is undefined or null");
  }
} else {
  console.log("which_row_to_delete is not a valid array or is empty");
}

await Dbms_table.updateMany({table_name : req?.body?.from_which_table}, {actual_data : new_row_with_filtered })
let result = await Dbms_table.find({table_name : req?.body?.from_which_table})
res.send({ status: 200, success: true, data: result, row_index :  req?.body?.which_row_to_delete});
});
routes.post("/clear", async (req, res) => {
await Dbms_table.updateMany({table_name : req?.body?.which_table_to_clear},{$set : {actual_data : []}} )

res.send({ status: 200, success: true, data: req?.body?.which_table_to_clear });
});

routes.put('/', async (req, res) => {
    try {
      let result = await Dbms_table.find({ table_name: req.body.table_name.trim() });
  
      if (result?.length > 0) {
        const reqBodyKeys = Object.keys(req.body).filter((key) => key !== 'table_name');
        // console.log(reqBodyKeys)
  
        if (reqBodyKeys?.length !== result[0]?.property_lst?.length) {
          return res.status(400).json({ status: 400, success: false, msg: `Number of properties is incorrect, Expected ${result[0]?.property_lst?.length} properties` });
        }
  
        let status = 200;
        let success = true;
        let msg = 'Data insert Successfully';
  
        // Extract values excluding table_name
        const actualDataObject = Object.fromEntries(Object.entries(req.body).filter(([key]) => key !== 'table_name'));
  
        // Additional checks for data type and max character length
        for (const [key, value] of Object.entries(actualDataObject)) {
          const propIndex = parseInt(key.replace('prop', ''), 10);
          const prop = result[0]?.property_lst[propIndex];
  
          if (typeof value !== prop.type) {
            status = 400;
            success = false;
            msg = `${key} has an unexpected type. Expected: ${prop.type}, Actual: ${typeof value}`;
            break;
          } else if (
            (typeof value === 'string' && value.length > prop.count) ||
            (typeof value === 'number' && value.toString().length > prop.count)
          ) {
            status = 400;
            success = false;
            msg = `${key} exceeds the maximum allowed length. Maximum: ${prop.count}, Actual: ${value.toString().length}`;
            break;
          }
        }
  let insetedData;
  let propertiesArray;
        // If there are no errors, append the object to the actual-data array
        if (success) {
          await Dbms_table.updateMany(
            { table_name: req.body.table_name },
            { $push: { 'actual_data': actualDataObject } }
          );
          insetedData = actualDataObject;
          propertiesArray = result[0]?.property_lst
        }
  
        return res.status(status).json({ status, success, msg, insetedData, propertiesArray});
      } else {
        res.status(400).json({ status: 400, success: false, msg: `No item created with name ${req.body.table_name.trim()}` });
      }
    } catch (error) {
      console.error(error);
      return res.status(500).json({ status: 500, success: false, msg: 'Internal Server Error' });
    }
  });
  
  
  
module.exports = routes;