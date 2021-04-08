describe('Full Text Search', function () {
  it('Displays the home page.', function () {
    cy.visit('/');
    cy.get('h1').should('contain', 'Full Text Search');
  });
});