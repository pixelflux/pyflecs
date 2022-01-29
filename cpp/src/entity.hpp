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
#include "component.hpp"
#include <string>


namespace pyflecs {
    /**
     * Approximates the flecs C++ class interface for an entity.
     */
    class entity final {
    public:
        entity(ecs_world_t* world, ecs_entity_t e);
        ~entity();

        bool is_alive()
        {
            return ecs_is_alive(mpWorld, mRaw);
        }

        void destruct()
        {
            ecs_delete(mpWorld, mRaw);
        }

        std::string name()
        {
            return std::string(ecs_get_name(mpWorld, mRaw));
        }

        ecs_entity_t raw()
        {
            return mRaw;
        }

        void add(component &c)
        {
            ecs_add_id(mpWorld, mRaw, c.raw());
        }

        void set(component& c, const void* bytes)
        {
            ecs_set_id(mpWorld, mRaw, c.raw(), c.size(), bytes);
        }

        const void* get(component& c)
        {
            return ecs_get_id(mpWorld, mRaw, c.raw());
        }

        void remove(component& c)
        {
            ecs_remove_id(mpWorld, mRaw, c.raw());
        }

    private:
        ecs_world_t* mpWorld;
        ecs_entity_t mRaw;

    };
}
