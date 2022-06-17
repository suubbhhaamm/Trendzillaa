import React from 'react'
import { Container, Row, Col } from 'react-bootstrap'

function Footer() {
  return (
    <div className="headerBackColor">
        <footer>
          <Container >
            <Row>
              <Col className="text-center py-3" style={{color: "white"}}>Copyright &copy; Trendzilla</Col>
            </Row>
          </Container>
        </footer>
    </div>
  )
}

export default Footer