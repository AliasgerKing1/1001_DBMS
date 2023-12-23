else {
    const document = await Dbms_table.findOne({ "property_lst.name": body?.what_to_select });

if (document) {
const index = document.property_lst.findIndex((property) => property.name === body?.what_to_select);

if (index !== -1 && document.actual_data) {
    // Extract the selected property from all objects in actual_data
    const selectedData = document.actual_data.map((obj) => obj[`prop${index}`]);
    res.send({ status: 200, success: true, data: { selectedData, matchedPropertyName: body?.what_to_select } });
} else {
    res.send({ status: 200, success: true, data: {} });
}
} else {
res.send({ status: 200, success: true, data: {} });
}


        }