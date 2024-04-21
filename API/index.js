var express = require("express")
var Mongoclient = require("mongodb").MongoClient
var cors = require("cors")
const multer = require("multer")

var app = express()
app.use(cors())

var CONNECTION_STRING = "mongodb+srv://justynvelasquez21:mD7U6aWhv0SnX5Nd@pf-database.9vxp59u.mongodb.net/?retryWrites=true&w=majority&appName=PF-Database"

var dbname = "stock"
var database

app.listen(5038,()=>{
    Mongoclient.connect(CONNECTION_STRING, (error,client)=>{
        database = client.db(dbname)
        console.log("Connected")
    })
})


app.get("/",(request,response)=>{
    response.send("Backend-Armed")
})

app.get("/api/PF/getStocks/:stock",(request,response)=>{
    database.collection(request.params.stock).find({}).toArray((error,result)=>{
        response.send(result)
    })
})

