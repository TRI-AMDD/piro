import '@testing-library/jest-dom';
import React from 'react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { render, screen } from '@testing-library/react';
import { MockQuery } from 'utils/Testing';
import Cats from './Cats';

const server = setupServer(
    rest.get('/cats.json', (req, res, ctx) => {
        return res(
            ctx.json([
                { _id: '1', text: 'cats are fun' },
                { _id: '2', text: 'cats are mean' }
            ])
        );
    })
);

// Enable API mocking before tests.
beforeAll(() => server.listen());

// Reset any runtime request handlers we may add during the tests.
afterEach(() => server.resetHandlers());

// Disable API mocking after the tests are done.
afterAll(() => server.close());

test('renders list of cats', async () => {
    render(
        <MockQuery>
            <Cats />
        </MockQuery>
    );

    const cat1 = await screen.findByText('cats are mean');

    // Check the other cat
    expect(cat1).toBeInTheDocument();
    const cat2 = await screen.getByText('cats are fun');
    expect(cat2).toBeInTheDocument();
});
