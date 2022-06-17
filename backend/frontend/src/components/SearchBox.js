import React, { useState } from 'react'
import { Button, Form } from 'react-bootstrap'
import { useNavigate, useLocation } from 'react-router-dom'

function SearchBox() {
    const [keyword, setKeyword] = useState('')

    let navigate = useNavigate()
    const location = useLocation();

    const submitHandler = (e) => {
        e.preventDefault()
        if (keyword) {
            navigate(`/?keyword=${keyword}&page=1`)
        } else {
            navigate(navigate(location.pathname))
        }
        this.keyword.value = "";
    }

    function handleSubmit(){
        this.keyword.value = "";
    }

    return (
        <Form onSubmit={submitHandler} className = 'd-flex'>
            <Form.Control
                type='text'
                name='q'
                onChange={(e) => setKeyword(e.target.value)}
                className='mr-sm-2 ml-sm-5'
            ></Form.Control>

            <Button
                type='submit'
                variant='outline-success'
                className='p-2'
                style={{color: "#d6abba",border:"none"}}
                onClick={handleSubmit}
            >
                Search
            </Button>
        </Form>
    )
}

export default SearchBox