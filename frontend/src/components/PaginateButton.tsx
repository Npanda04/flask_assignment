
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';

export const PaginatedButton = ({ currentPage, totalPages, onPrevious, onNext }) => {
  const navigate = useNavigate();

  const handlePageChange = (newPage) => {
    navigate(`?page=${newPage}`);
    if (newPage < currentPage) {
      onPrevious(newPage);
    } else {
      onNext(newPage);
    }
  };

  const handlePrevious = () => {
    const prevPage = currentPage > 1 ? currentPage - 1 : 1;
    handlePageChange(prevPage);
  };

  const handleNext = () => {
    const nextPage = currentPage < totalPages ? currentPage + 1 : totalPages;
    handlePageChange(nextPage);
  };

  return (
    <div>
      <Button size="sm" onClick={handlePrevious} disabled={currentPage === 1}>
        Previous
      </Button>
      <span> Page {currentPage} of {totalPages} </span>
      <Button size="sm" onClick={handleNext} disabled={currentPage === totalPages}>
        Next
      </Button>
    </div>
  );
};


