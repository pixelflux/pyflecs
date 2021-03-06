/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#pragma once

#include "flecs.h"
#include "entity.hpp"
#include "filter.hpp"
#include "query.hpp"

#include <string>
#include <vector>
#include <iostream>

/**
 * Approximates the flecs C++ class interface for the world.
 */
namespace pyflecs {

    class world final {
    public:
        world();
        ~world();

        pyflecs::entity entity();
        pyflecs::entity entity(std::string name);
        pyflecs::entity entity(pyflecs::entity& c);
        pyflecs::entity lookup(std::string name);
        pyflecs::entity lookup_path(std::string name);
        pyflecs::id lookup_by_id(ecs_id_t eid);

        std::vector<pyflecs::entity> bulk_entity_w_id(ecs_id_t eid,
            int32_t count);
        pyflecs::bulk_entity_builder bulk_entity_builder(int32_t count);

        pyflecs::entity component(std::string name, size_t size, 
            size_t alignment);

        pyflecs::filter create_filter(std::string name, std::string expr, 
            bool instanced, std::vector<ecs_term_t> terms);
        pyflecs::query create_query(std::string name, std::string expr,
            bool instanced, std::vector<ecs_term_t> terms);

        pyflecs::iter create_term_iter(ecs_term_t* term)
        {
            return pyflecs::iter(ecs_term_iter(mpRaw, term));
        }

        ecs_world_t* raw()
        {
            return mpRaw;
        }

    private:
        ecs_world_t *mpRaw;

    };
}
