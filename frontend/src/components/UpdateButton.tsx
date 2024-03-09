import React from 'react';
import { Button } from './ui/button';
import { Link } from 'react-router-dom';

export const UpdateButton = ({ to }) => (
  <Link to={to}>
    <Button size="lg" variant="default">
      Update
    </Button>
  </Link>
);


