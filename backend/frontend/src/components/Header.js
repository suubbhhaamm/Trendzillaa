import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Navbar, Nav, Container, Row, NavDropdown } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import SearchBox from './SearchBox'
import { logout } from '../actions/userActions'

function Header() {

    const userLogin = useSelector(state => state.userLogin)
    const { userInfo } = userLogin

    const dispatch = useDispatch()

    const logoutHandler = () => {
        dispatch(logout())
    }


    return (
        <header>
          <Navbar className="headerBackColor" expand="lg" collapseOnSelect>
              <Container>
                <LinkContainer to='/'>
                  <Navbar.Brand> <img src="https://fontmeme.com/permalink/220616/076bcd7729ec701ca58d3dff92010842.png" alt="Trendzilla" style={{height:"40px"}}/> </Navbar.Brand>
                </LinkContainer>
                
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                  <SearchBox/>
                  <Nav className="ml-auto">
                    
                    <LinkContainer to='/cart' style={{color: "white"}}>
                      <Nav.Link><i className="fas fa-shopping-cart" style={{color: "white"}}></i>Cart </Nav.Link>
                    </LinkContainer>


                    {userInfo ? (
                      <NavDropdown title={userInfo.name} id='username' style={{color: "white"}}>
                        <LinkContainer to='/profile' >
                          <NavDropdown.Item>Profile</NavDropdown.Item>
                        </LinkContainer>

                        <NavDropdown.Item onClick={logoutHandler}>Logout</NavDropdown.Item>

                        </NavDropdown>
                    ) : (
                          <LinkContainer to='/login' style={{color: "white"}}>
                            <Nav.Link> <i className="fas fa-user" style={{color: "white"}}></i>Login</Nav.Link>
                          </LinkContainer>
                    )}


                    {userInfo && userInfo.isAdmin && (
                        <NavDropdown title='Admin' id='adminmenue' style={{color: "white"}}>
                            <LinkContainer to='/admin/userlist'>
                                <NavDropdown.Item>Users</NavDropdown.Item>
                            </LinkContainer>

                            <LinkContainer to='/admin/productlist'>
                                <NavDropdown.Item>Products</NavDropdown.Item>
                            </LinkContainer>

                            <LinkContainer to='/admin/orderlist'>
                                <NavDropdown.Item>Orders</NavDropdown.Item>
                            </LinkContainer>

                        </NavDropdown>
                    )}
                    
                  </Nav>
                </Navbar.Collapse>
              </Container>
          </Navbar>
        </header>
    )
}

export default Header
