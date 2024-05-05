const mongoose = require('mongoose');

const db = async () => {
    try {
        mongoose.set('strictQuery', false)
        await mongoose.connect('mongodb+srv://dbuser:jUl2HxdcrbDF5maB@cluster0.dkpyzjk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        // await mongoose.connect('mongodb+srv://hackishmax321:111222333@cluster0.ubi66uf.mongodb.net/?retryWrites=true&w=majority')
        // mongodb+srv://dbuser:111222333@cluster0.eq38kl0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
        console.log('Db Connected')
    } catch (error) {
        console.log('DB Connection Error');
    }
}

module.exports = {db}