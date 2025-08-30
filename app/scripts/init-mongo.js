db = db.getSiblingDB(ProcessingInstruction.env.MONGO_DB || 'catalog')
try{
    db.createUser({
        user: ProcessingInstruction.env.MONGO_INITDB_ROOT_USERNAME || 'catalog_user',
        pwd: ProcessingInstruction.env.MONGO_INITDB_ROOT_PASSWORD || 'catalog_pass',
        roles: [{
            role: 'readWrite',
            db: ProcessingInstruction.env.MONGO_DB || 'catalog_api'}]
    })
}
catch (e) {
    if (e.codeName !== 'UserAlreadyExists') {
        throw e;
    }
}   

const products = db.getCollection('products')
products.createIndex({product_id: 1}, {unique: true})
products.createIndex({categories: 1})
products.createIndex({brand:1})
products.createIndex({price: 1})
products.createIndex({name: 'text', description: 'text', brand: 'text'});