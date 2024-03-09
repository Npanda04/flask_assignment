import { CardTitle, CardDescription, CardHeader, CardContent, CardFooter, Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TableHead, TableRow, TableHeader, TableCell, TableBody, Table } from "@/components/ui/table";
import { useEffect, useState } from "react";
import axios from "axios";
import { BACKEND_URL } from "@/config";
import { Link } from "react-router-dom";
import { PaginatedButton } from "./PaginateButton";
import { UpdateButton } from "./UpdateButton";
import { DeleteButton } from "./DeleteButton";
import {useNavigate} from "react-router-dom"

export const UserDetailComponent = () => {
  const navigate = useNavigate()


  const handlePrevious = () => {
    setPagination({ ...pagination, page: Math.max(pagination.page - 1, 1) });
  };

  const handleNext = () => {
    setPagination({ ...pagination, page: Math.min(pagination.page + 1, pagination.total_pages) });
  };


  const userDetail = async () => {
    const response = await axios.get(`${BACKEND_URL}/api/v1/user?page=${pagination.page}`);
    setUsers(response.data.users);
    console.log(response.data.users)
    setPagination({
      ...pagination,
      total_pages: response.data.pagination.total_pages,
      total_items: response.data.pagination.total_items,
    });
  };




  const handleDelete = async (userId) => {

    
    try {
      // Send DELETE request to the server
      await axios.delete(`${BACKEND_URL}/api/v1/user/${userId}`);
      userDetail()
      navigate("/")
      console.log("called delte ")
      
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };


 



  const [users, setUsers] = useState([]);
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 5,
    total_pages: 1,
    total_items: 0,
  });


  

  useEffect(() => {
    
    userDetail();
    console.log("called datat fetch ")
  }, [pagination.page]); // Update the user data when the page changes



  return (
    <Card>
      <CardHeader>
        <CardTitle>User Management</CardTitle>
        <CardDescription>Manage users in the system.</CardDescription>
      </CardHeader>
      <CardContent className="mt-4">
        <div className="flex items-center space-x-2 mb-4">
          <Link to="/userform">
            <Button size="lg" variant="default">
              Add User
            </Button>
          </Link>
        </div>
        <div className="overflow-auto h-[400px] border rounded-lg">
          <Table className="w-full">
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Username</TableHead>
                <TableHead>Place</TableHead>
                <TableHead>Amount</TableHead>
                <TableHead>Action</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>

            <TableBody>
              {users.map((user) => (
                <TableRow key={user.id}>
                  <TableCell className="font-semibold">
                    {user.firstname} {user.lastname}
                  </TableCell>
                  <TableCell>{user.username}</TableCell>
                  <TableCell>{user.place}</TableCell>
                  <TableCell>{user.amount}</TableCell>
                  <TableCell>

                    <DeleteButton onClick={() => handleDelete(user.id)}/>
                  </TableCell>
                  <TableCell>
                    
                      <UpdateButton to={`/userform/${user.id}`} />

                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
      <CardFooter>
        <div className="flex items-center justify-between w-full max-w-sm mx-auto">
          <div className="flex items-center space-x-2">
            <PaginatedButton currentPage={pagination.page} totalPages={pagination.total_pages} onPrevious={handlePrevious} onNext={handleNext} />
          </div>
        </div>
      </CardFooter>
    </Card>
  );
};
