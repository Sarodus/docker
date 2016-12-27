from .base import Component

class Media(Component):

    type = "media"

    def _index(self):
        return '''
        <div class="row">
            <div class="col-xs-12">
                <h2>Hey!</h2>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ultrices laoreet egestas. Nam vitae ultrices lectus, nec pulvinar purus. In dictum sapien risus, eget ultricies turpis sollicitudin quis. Curabitur porta lacus imperdiet leo varius efficitur. Etiam non dapibus velit. Aliquam erat volutpat. Morbi fermentum ipsum nec nibh scelerisque condimentum. Donec vel quam nisl. Etiam bibendum eros at ex ultricies, eu feugiat sapien mattis. Quisque maximus est sollicitudin sagittis maximus. Phasellus sed metus sit amet diam posuere dignissim. Curabitur fringilla posuere mi in bibendum.</p>
            </div>
        </div>
        '''


    def index(self):
        return self._render_template('wrapper.html', body=self._default())
