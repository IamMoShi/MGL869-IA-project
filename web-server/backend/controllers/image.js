const uploadSF = require("../models/bucket");

module.exports = {
    list: async (req, res) => {
        const data = await uploadSF.imageslist(req, res);
        console.log(data);
        res.status(400).json({ mgs: "erreur" });
    },
};
