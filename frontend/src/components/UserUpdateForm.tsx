


import { CardTitle, CardDescription, CardHeader, CardContent, CardFooter, Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useNavigate , useParams} from "react-router-dom"


import { useState } from "react"
import { BACKEND_URL } from "@/config"
import axios from "axios"

export const UserUpdateForm = () => {

    const navigate = useNavigate()

    const { userId } = useParams();

  

    const [postInputs, setPostInputs] = useState({
        firstname: "",
        lastname: "",
        username: "",
        place: "",

    })


    async function sendUpdateUserRequest() {
        try {
            const response = await axios.put(`${BACKEND_URL}/api/v1/user/${userId}`, postInputs)
            console.log(response.data)
            navigate("/")
        } catch (error) {
            console.log("error while loggining in")
        }
    }
    return (
        <main className="flex items-center justify-center h-screen">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-2xl">Updated User</CardTitle>
                    <CardDescription>Fill out the form below to udpate the user.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="first-name">First name</Label>
                            <Input onChange={(e) => {
                                setPostInputs({
                                    ...postInputs,
                                    firstname: e.target.value
                                })
                            }} id="first-name" placeholder="Enter your first name" />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="last-name">Last name</Label>
                            <Input onChange={(e) => {
                                setPostInputs({
                                    ...postInputs,
                                    lastname: e.target.value

                                })

                            }} id="last-name" placeholder="Enter your last name" />
                        </div>
                        <div className="space-y-2 col-span-2">
                            <Label htmlFor="username">Username</Label>
                            <Input onChange={(e) => {
                                setPostInputs({
                                    ...postInputs,
                                    username: e.target.value

                                })

                            }} id="username" placeholder="Enter your username" />
                        </div>
                        <div className="space-y-2 col-span-2">
                            <Label htmlFor="place">Place</Label>
                            <Input onChange={(e) => {
                                setPostInputs({
                                    ...postInputs,
                                    place: e.target.value
                                })
                            }} id="place" placeholder="Enter your place" />
                        </div>
                    </div>
                </CardContent>
                <CardFooter>
                    <Button onClick={sendUpdateUserRequest} className="ml-auto">Update User</Button>
                </CardFooter>
            </Card>
        </main>
    )
}




