import {useEffect, useState} from 'react' 

function GiftList() {

    const [gifts, setGifts] = useState([])

    useEffect(() => {
        fetch('/gifts')
        .then(res => res.json())
        .then(data => setGifts(data))
    }, [])

    const mappedGifts = gifts.map(g => <li>{g.name} - ${g.price}</li>)

    return (
        <div>

            { mappedGifts }

        </div>
    )
}

export default GiftList