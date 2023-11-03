import React from 'react';
import ReactDOM from 'react-dom';
import { ReactiveBase, ReactiveList, DataSearch } from '@appbaseio/reactivesearch';
import './index.css';

class Main extends React.Component {
  render() {
    return (
      <ReactiveBase
        app="hotels" // Nombre de tu aplicación de Elasticsearch
        url="http://localhost:9200" // URL de tu instancia de Elasticsearch
      >
        <DataSearch
          componentId="SearchSensor"
          dataField={['nombre']} // Campo por el que se va a buscar
          placeholder="Buscar por nombre" // Mensaje del input de búsqueda

        />
        <ReactiveList
          react={{and:["SearchSensor"]}}
          size={100}
          pagination={true}
          componentId="SearchResult"
          dataField="nombre" // Campo que quieres mostrar
          renderItem={(res) => (
            <div key={res._id}>
              <p>{res.nombre}</p> {/* Mostrar el campo 'nombre' */}
            </div>
          )}
        />
      </ReactiveBase>
    );
  }
}

ReactDOM.render(<Main />, document.getElementById('root'));


