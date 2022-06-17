import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Row, Col } from 'react-bootstrap'
import { useLocation } from 'react-router-dom'
import Product from '../components/Product'
import Loader from '../components/Loader'
import Message from '../components/Message'
import Paginate from '../components/Paginate'
import ProductCarousel from '../components/ProductCarousel'
// import RecommendProduct from '../components/RecommendProduct'
import { listProducts, listMenProducts } from '../actions/productActions'




function HomeScreen() {

  const dispatch = useDispatch()
  const productList = useSelector(state => state.productList)
  const { error, loading, products, page, pages } = productList

  /* const menProductList = useSelector(state => state.menProductList)
  const { error1, loading1, products1, page1, pages1 } = menProductList */

  const location = useLocation()
  let keyword = location.search
  

  useEffect(() => {
    dispatch(listProducts(keyword))
    //dispatch(listMenProducts(keyword))

  }, [dispatch, keyword])

  


  return (
    <div>

      {!keyword && pages && <ProductCarousel />}

      <h1>Latest Products</h1>
        {loading ? <Loader />
          : error ? <Message variant='danger'>{error}</Message>
            :
              <div>
                <Row>
                  {products.map(product => (
                    <Col key={product._id} sm={12} md={6} lg={4} xl={3}>
                      <Product product={product} />
                    </Col>
                  ))}
                </Row>

                  <Paginate page={page} pages={pages} keyword={keyword}/>

              </div>
        }

        {/* {!keyword && pages && <RecommendProduct />} */}

    </div>
  )
}

export default HomeScreen
